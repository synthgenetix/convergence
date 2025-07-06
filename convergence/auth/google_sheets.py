"""
📊 Google Sheets integration for API key management
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from convergence.auth.models import APIKey
from convergence.utils.console import console, print_error, print_success, print_warning


class GoogleSheetsClient:
    """Client for interacting with Google Sheets API"""

    def __init__(self, credentials_path: Optional[str] = None, sheet_id: Optional[str] = None):
        self.credentials_path = credentials_path or os.getenv("GOOGLE_CREDENTIALS_PATH")
        self.sheet_id = sheet_id or os.getenv("GOOGLE_SHEET_ID")
        self.sheet_name = os.getenv("GOOGLE_SHEET_NAME", "API_Keys")
        self.service = None
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize the Google Sheets client"""
        if self._initialized:
            return True

        if not self.credentials_path or not self.sheet_id:
            print_warning(
                "Google Sheets credentials or sheet ID not configured", "Authentication Setup"
            )
            return False

        try:
            # Load credentials
            creds_path = Path(self.credentials_path)
            if not creds_path.exists():
                print_error(
                    f"Credentials file not found: {self.credentials_path}", "Authentication Error"
                )
                return False

            # Create credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
            )

            # Build service
            self.service = build("sheets", "v4", credentials=credentials)
            self._initialized = True

            print_success(f"Connected to Google Sheets: {self.sheet_id}", "Authentication Ready")
            return True

        except Exception as e:
            print_error(
                f"Failed to initialize Google Sheets client: {str(e)}", "Authentication Error"
            )
            return False

    def fetch_api_keys(self) -> List[APIKey]:
        """Fetch all API keys from Google Sheets"""
        if not self._initialized:
            if not self.initialize():
                return []

        try:
            # Define the range to read (assuming headers in row 1)
            range_name = f"{self.sheet_name}!A2:F"

            # Execute the request
            if not self.service:
                return []

            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=self.sheet_id, range=range_name)
                .execute()
            )

            values = result.get("values", [])
            api_keys = []

            for row in values:
                if len(row) >= 5:  # Ensure we have all required fields
                    try:
                        api_key = APIKey(
                            api_key=row[0],
                            client_name=row[1],
                            created_at=datetime.fromisoformat(row[2]),
                            expires_at=datetime.fromisoformat(row[3]) if row[3] else None,
                            is_active=row[4].lower() == "true",
                            rate_limit=int(row[5]) if len(row) > 5 and row[5] else None,
                        )
                        api_keys.append(api_key)
                    except (ValueError, IndexError) as e:
                        console.print(
                            f"   ⚠️  Skipping invalid row: {row[:2]}... - {str(e)}",
                            style="yellow dim",
                        )

            console.print(f"   📊 Loaded {len(api_keys)} API keys from Google Sheets", style="dim")
            return api_keys

        except HttpError as e:
            print_error(f"Google Sheets API error: {str(e)}", "Authentication Error")
            return []
        except Exception as e:
            print_error(f"Failed to fetch API keys: {str(e)}", "Authentication Error")
            return []

    def get_api_key(self, api_key: str) -> Optional[APIKey]:
        """Get a specific API key"""
        api_keys = self.fetch_api_keys()
        for key in api_keys:
            if key.api_key == api_key:
                return key
        return None

    def validate_api_key(self, api_key: str) -> bool:
        """Validate if an API key exists and is valid"""
        key_obj = self.get_api_key(api_key)
        if not key_obj:
            return False
        return key_obj.is_valid()


# Global instance for caching
_sheets_client: Optional[GoogleSheetsClient] = None


def get_sheets_client() -> GoogleSheetsClient:
    """Get or create the global Google Sheets client"""
    global _sheets_client
    if _sheets_client is None:
        _sheets_client = GoogleSheetsClient()
    return _sheets_client
