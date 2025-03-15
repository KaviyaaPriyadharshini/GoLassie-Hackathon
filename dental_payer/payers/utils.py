from fuzzywuzzy import fuzz
from .models import Payer, PayerDetail, PayerGroup, get_default_payer_group
import re
import pandas as pd

def normalize_payer_name(name):
    return re.sub(r'[^A-Z0-9 ]', '', name.upper().strip()) if isinstance(name, str) else None

def create_or_get_payer_group(normalized_name):
    group_name = normalized_name.split()[0] 
    payer_group, created = PayerGroup.objects.get_or_create(name=group_name)
    return payer_group

def find_or_create_payer(name, payer_number, tax_id):
    normalized_name = normalize_payer_name(name)
    if payer_number:
        existing_detail = PayerDetail.objects.filter(payer_number=payer_number).first()
        if existing_detail:
            return existing_detail.payer 
    
    payer = Payer.objects.filter(name=normalized_name).first()
    if not payer:
        for existing_payer in Payer.objects.all():
            if fuzz.ratio(existing_payer.name, normalized_name) > 90:  
                return existing_payer  
    payer_group = create_or_get_payer_group(normalized_name)
    payer = Payer.objects.create(name=normalized_name, group=payer_group, pretty_name=name)
    
    return payer

def map_payer_details(raw_data):
    for data in raw_data:
        name = data.get('name')
        payer_number = data.get('payer_number')
        tax_id = data.get('tax_id')
        source = data.get('source')

        if not name:
            print("Skipping entry due to missing payer name.")
            continue

        normalized_name = normalize_payer_name(name)
        payer = find_or_create_payer(normalized_name, payer_number, tax_id)
        if not PayerDetail.objects.filter(payer=payer, payer_number=payer_number, tax_id=tax_id).exists():
            PayerDetail.objects.create(
                payer=payer,
                payer_number=payer_number,
                tax_id=tax_id,
                source=source
            )

def process_uploaded_file(file):
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
