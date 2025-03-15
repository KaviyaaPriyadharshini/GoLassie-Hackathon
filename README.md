# GoLassie Hackathon - Dental Insurance Payer Processing System

## Overview

This project is designed to tackle challenges in the dental insurance industry related to the processing of payments from insurance companies. The system effectively handles payer information, deduplication, and standardized display names for a seamless user experience.

## Tech Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite3

## Mapping Logic

1. **Normalize Payer Name**: Cleans and standardizes payer names for consistent storage and comparison.
2. **Create or Get Payer Group**: Ensures each payer is associated with a relevant group, creating one if necessary.
3. **Find or Create Payer**: Searches for existing payers and creates new ones using fuzzy matching to handle similar names.
4. **Map Payer Details**: Processes raw data and maps it to the database while avoiding duplicates.
5. **Process Uploaded File**: Handles Excel file uploads, extracting and storing payer information in the database.
