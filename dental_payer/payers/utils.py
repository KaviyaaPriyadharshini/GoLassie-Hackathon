from .models import Payer, PayerDetail, PayerGroup, get_default_payer_group
import pandas as pd
import re
from fuzzywuzzy import fuzz

def normalize_payer_name(name):
    """
    Normalize payer name by stripping whitespace, converting to uppercase,
    and removing special characters.
    """
    return re.sub(r'[^A-Z0-9 ]', '', name.upper().strip()) if isinstance(name, str) else None

def create_or_get_payer_group(normalized_name):
    """
    Create or get a payer group based on the normalized payer name.
    """
    # Generate a group name based on the normalized payer name
    group_name = normalized_name.split()[0]  # Use the first word as the group name
    payer_group, created = PayerGroup.objects.get_or_create(name=group_name)
    return payer_group

def find_or_create_payer(name, payer_number, tax_id):
    """
    Find an existing payer or create a new one, assigning it to a dynamically created payer group.
    """
    # Check for existing payer details by payer number
    if payer_number:
        existing_detail = PayerDetail.objects.filter(payer_number=payer_number).first()
        if existing_detail:
            return existing_detail.payer 

    # Normalize the payer name
    normalized_name = normalize_payer_name(name)
    
    # Check for existing payer by normalized name
    payer = Payer.objects.filter(name=normalized_name).first()

    # If no payer found, check for fuzzy matches
    if not payer:
        for existing_payer in Payer.objects.all():
            if fuzz.ratio(existing_payer.name, normalized_name) > 90:
                return existing_payer 

    # Create or get a payer group based on the normalized name
    payer_group = create_or_get_payer_group(normalized_name)

    # Create the payer
    payer = Payer.objects.create(name=normalized_name, group=payer_group, pretty_name=name)

    return payer

def map_payer_details(raw_data):
    """
    Process and deduplicate payer details from raw data.
    """
    for data in raw_data:
        name = data.get('name')
        payer_number = data.get('payer_number')
        tax_id = data.get('tax_id')
        source = data.get('source')

        if not name:
            print("Skipping entry due to missing payer name.")
            continue

        normalized_name = normalize_payer_name(name)

        # Find or create payer
        payer = find_or_create_payer(normalized_name, payer_number, tax_id)

        # Check if the payer detail already exists
        if not PayerDetail.objects.filter(payer=payer, payer_number=payer_number, tax_id=tax_id).exists():
            PayerDetail.objects.create(
                payer=payer,
                payer_number=payer_number,
                tax_id=tax_id,
                source=source
            )

def process_uploaded_file(file):
    """
    Process uploaded Excel file and map payers while ensuring deduplication.
    """
    try:
        df = pd.read_excel(file)
        df.columns = [str(col).strip().lower() for col in df.columns]

        print("Columns found:", df.columns.tolist())  
        payer_number_column = None
        payer_name_column = None
        for col in df.columns:
            if 'payer id' in col or 'id' in col:
                payer_number_column = col
                break

        for col in df.columns:
            if 'payer identification information' in col or 'payer' in col or  'payer name' in col:
                payer_name_column = col
                break    
        for _, row in df.iterrows():
            payer_name = row.get(payer_name_column, '').strip() if payer_name_column in df.columns else None
            payer_number = row.get(payer_number_column, '') if payer_number_column in df.columns else None
            tax_id = row.get('tax id', '') if 'tax id' in df.columns else None
            source = row.get('source', 'Uploaded File')

            if not payer_name:
                print("Skipping row with empty payer name.")
                continue

            normalized_name = normalize_payer_name(payer_name)

            # Find or create payer
            payer = find_or_create_payer(normalized_name, payer_number, tax_id)

            if payer and payer_number:
                if not PayerDetail.objects.filter(payer=payer, payer_number=payer_number, tax_id=tax_id).exists():
                    PayerDetail.objects.create(
                        payer=payer,
                        payer_number=payer_number,
                        tax_id=tax_id,
                        source=source
                    )

        return "File processed successfully!"
    except Exception as e:
        return f"Error processing file: {e}"