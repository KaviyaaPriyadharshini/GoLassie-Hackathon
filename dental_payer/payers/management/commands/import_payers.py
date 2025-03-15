import csv
import os
from django.core.management.base import BaseCommand
from payers.utils import map_payer_details

class Command(BaseCommand):
    help = 'Import payer details from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='Name of CSV file in management/commands folder')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the commands directory
        file_path = os.path.join(base_dir, file_name)  # Construct full path

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_name} not found in {base_dir}"))
            return

        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = [row for row in reader]
        except UnicodeDecodeError:
            self.stdout.write(self.style.ERROR(f"Error reading {file_name}. Ensure it is saved as UTF-8."))
            return

        map_payer_details(data)
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(data)} payer records from {file_path}'))
