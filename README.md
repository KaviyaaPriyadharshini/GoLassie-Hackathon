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

# API Endpoints

This section lists the available API endpoints for managing payers.

## Base URL
`/api/`

### Payer Endpoints
- **List Payers**
  - **GET** `/api/payers/`
- **Create Payer**
  - **POST** `/api/payers/`
- **Retrieve Payer**
  - **GET** `/api/payers/{id}/`
- **Update Payer**
  - **PUT** `/api/payers/{id}/`
- **Delete Payer**
  - **DELETE** `/api/payers/{id}/`
  
### Payer Detail Endpoints
- **List Payer Details**
  - **GET** `/api/payer_details/`
- **Retrieve Payer Detail**
  - **GET** `/api/payer_details/{id}/`
    
### Additional Endpoints
- **Manual Mapping**
  - **POST** `/api/manual_mapping/`
- **Upload Payer File**
  - **POST** `/api/upload/`
- **Manage Payer Groups**
  - **GET/POST** `/api/manage_payer_groups/`
- **Edit Payer Group**
  - **PUT** `/api/edit_payer_group/{group_id}/`
- **Delete Payer Group**
  - **DELETE** `/api/delete_payer_group/{group_id}/`
- **Payer Hierarchy**
  - **GET** `/api/payer_hierarchy/`
- **Edit Payer**
  - **PUT** `/api/edit_payer/{payer_id}/`
- **Delete Payer**
  - **DELETE** `/api/delete_payer/{payer_id}/`
- **Unmap Payer**
  - **POST** `/api/unmap_payer/`
