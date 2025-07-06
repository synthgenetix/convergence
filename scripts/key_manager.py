import os
import sys
import argparse
from typing import List, Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from dotenv import load_dotenv

DEFAULT_ENVIRONMENT = "local"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_HEADERS = ["key_id", "api_key", "created_at", "actor", "expires_at"]
DEFAULT_SHEET_NAME = "CONVERGENCE_API_KEYS"


def load_env(environment: str = DEFAULT_ENVIRONMENT):
    """
    Load environment variables from .env.{environment} or .env file.
    """
    print(f"Loading environment: .env.{environment}.")
    try:
        is_loaded = load_dotenv(f".env.{environment}", override=True)
        if not is_loaded:
            print(f"No .env.{environment} file found, trying .env file.")
            is_loaded = load_dotenv(f".env", override=True)
            if not is_loaded:
                raise ValueError(f"No .env.{environment} or .env file found.")
    except Exception as e:
        print(f"Error loading environment variables for '{environment}': {e}")
        sys.exit(1)


def get_creds() -> Credentials:
    """
    Get credentials from environment variables or create them if they don't exist.
    """
    creds_path = os.getenv("GDRIVE_CREDENTIALS_JSON")
    token_path = os.getenv("GDRIVE_TOKEN_JSON")

    if not creds_path:
        raise ValueError("Missing GDRIVE_CREDENTIALS_JSON environment variable.")

    if os.path.exists(token_path or ""):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
        creds = flow.run_local_server(port=0)
        if token_path:
            with open(token_path, "w") as token_file:
                token_file.write(creds.to_json())

    return creds


def get_sheets_service():
    creds = get_creds()
    return build("sheets", "v4", credentials=creds)


def get_or_create_sheet(spreadsheet_id: str, sheet_name: str = DEFAULT_SHEET_NAME):
    service = get_sheets_service()
    sheets = service.spreadsheets()
    metadata = sheets.get(spreadsheetId=spreadsheet_id).execute()
    sheet_names = [s["properties"]["title"] for s in metadata["sheets"]]

    if sheet_name not in sheet_names:
        requests = [{"addSheet": {"properties": {"title": sheet_name}}}]
        sheets.batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": requests}).execute()
        sheets.values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A1:E1",
            valueInputOption="RAW",
            body={"values": [SHEET_HEADERS]},
        ).execute()

    return sheet_name


def read_all_rows(spreadsheet_id: str, sheet_name: str) -> List[List[str]]:
    service = get_sheets_service()
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!A2:E")
        .execute()
    )
    return result.get("values", [])


def find_row_index_by_key(spreadsheet_id: str, sheet_name: str, key_id: str) -> Optional[int]:
    rows = read_all_rows(spreadsheet_id, sheet_name)
    for i, row in enumerate(rows):
        if row and row[0] == key_id:
            return i + 2  # because sheet index starts from 1 and headers are in row 1
    return None


def list_keys(spreadsheet_id: str, sheet_name: str):
    rows = read_all_rows(spreadsheet_id, sheet_name)
    for row in rows:
        print(dict(zip(SHEET_HEADERS, row)))


def search(spreadsheet_id: str, sheet_name: str, key: str):
    rows = read_all_rows(spreadsheet_id, sheet_name)
    for row in rows:
        if any(key in cell for cell in row):
            print(dict(zip(SHEET_HEADERS, row)))


def search_by(spreadsheet_id: str, sheet_name: str, field: str, value: str):
    idx = SHEET_HEADERS.index(field)
    rows = read_all_rows(spreadsheet_id, sheet_name)
    for row in rows:
        if len(row) > idx and row[idx] == value:
            print(dict(zip(SHEET_HEADERS, row)))


def update_key(spreadsheet_id: str, sheet_name: str, key_id: str, field: str, new_value: str):
    row_index = find_row_index_by_key(spreadsheet_id, sheet_name, key_id)
    if not row_index:
        print("Key ID not found.")
        return

    field_idx = SHEET_HEADERS.index(field)
    range_cell = f"{sheet_name}!{chr(65 + field_idx)}{row_index}"

    service = get_sheets_service()
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_cell,
        valueInputOption="RAW",
        body={"values": [[new_value]]},
    ).execute()
    print(f"Updated {field} for key {key_id} to {new_value}")


def delete_key(spreadsheet_id: str, sheet_name: str, key_id: str):
    row_index = find_row_index_by_key(spreadsheet_id, sheet_name, key_id)
    if not row_index:
        print("Key ID not found.")
        return

    requests = [
        {
            "deleteDimension": {
                "range": {
                    "sheetId": get_sheet_id(spreadsheet_id, sheet_name),
                    "dimension": "ROWS",
                    "startIndex": row_index - 1,
                    "endIndex": row_index,
                }
            }
        }
    ]
    service = get_sheets_service()
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={"requests": requests}
    ).execute()
    print(f"Deleted key with ID {key_id}")


def get_sheet_id(spreadsheet_id: str, sheet_name: str):
    service = get_sheets_service()
    metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for sheet in metadata["sheets"]:
        if sheet["properties"]["title"] == sheet_name:
            return sheet["properties"]["sheetId"]
    raise ValueError(f"Sheet {sheet_name} not found")


def main():
    load_env()

    parser = argparse.ArgumentParser(description="Manage API keys in Google Sheets.")
    parser.add_argument("--spreadsheet-id", required=True, help="Google Sheet ID")
    parser.add_argument("--sheet", default=DEFAULT_SHEET_NAME, help="Sheet name")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all API keys")

    search = subparsers.add_parser("search", help="General search across all fields")
    search.add_argument("query")

    sba = subparsers.add_parser("search-actor", help="Search by actor")
    sba.add_argument("actor")

    sbk = subparsers.add_parser("search-apikey", help="Search by API key")
    sbk.add_argument("api_key")

    update = subparsers.add_parser("update", help="Update a key field")
    update.add_argument("key_id")
    update.add_argument("field", choices=SHEET_HEADERS)
    update.add_argument("value")

    delete = subparsers.add_parser("delete", help="Delete a key by key_id")
    delete.add_argument("key_id")

    args = parser.parse_args()

    sheet_name = get_or_create_sheet(args.spreadsheet_id, args.sheet)

    if args.command == "list":
        list_keys(args.spreadsheet_id, sheet_name)
    elif args.command == "search":
        search(args.spreadsheet_id, sheet_name, args.query)
    elif args.command == "search-actor":
        search_by(args.spreadsheet_id, sheet_name, "actor", args.actor)
    elif args.command == "search-apikey":
        search_by(args.spreadsheet_id, sheet_name, "api_key", args.api_key)
    elif args.command == "update":
        update_key(args.spreadsheet_id, sheet_name, args.key_id, args.field, args.value)
    elif args.command == "delete":
        delete_key(args.spreadsheet_id, sheet_name, args.key_id)


if __name__ == "__main__":
    main()
