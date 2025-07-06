import mimetypes
import os
from pathlib import Path
from typing import Any, Optional, cast

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def load_credentials() -> Credentials:
    """
    Load Google Drive API credentials from environment variables.
    Required ENV:
    - GDRIVE_CREDENTIALS_JSON
    - GDRIVE_TOKEN_JSON
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

    return cast(Credentials, creds)


def build_drive_service(creds: Credentials) -> Any:
    """Build Google Drive API service."""
    return build("drive", "v3", credentials=creds)


def upload_audio_file(file_path: str, folder_id: Optional[str] = None, public: bool = False) -> str:
    """
    Upload an audio file to Google Drive.
    Returns the shareable URL.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("audio/"):
        raise ValueError(f"{file_path} is not an audio file.")

    creds = load_credentials()
    service = build_drive_service(creds)

    file_metadata = {
        "name": os.path.basename(file_path),
    }
    if folder_id:
        file_metadata["parents"] = [folder_id]  # type: ignore[assignment]

    media = MediaFileUpload(file_path, mimetype=mime_type)

    try:
        uploaded_file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id,webViewLink,webContentLink")
            .execute()
        )

        file_id = uploaded_file.get("id")
        view_url = uploaded_file.get("webViewLink")

        if public:
            set_file_public(service, file_id)
            return str(view_url)

        return str(view_url)

    except HttpError as error:
        raise RuntimeError(f"An error occurred: {error}")


def set_file_public(service: Any, file_id: str) -> None:
    """Set file permission to 'Anyone with the link can view'."""
    permission = {"type": "anyone", "role": "reader"}
    service.permissions().create(fileId=file_id, body=permission).execute()
