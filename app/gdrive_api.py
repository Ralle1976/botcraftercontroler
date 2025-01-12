import os
import io
import json
from googleapiclient.discovery import build
from googleapiclient.http import  MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account

def get_drive_service():
    # Lese die JSON-Datei aus der Umgebungsvariable
    credentials_info = os.getenv("GOOGLE_CREDENTIALS")
    if not credentials_info:
        raise RuntimeError("GOOGLE_CREDENTIALS environment variable is not set")

    credentials = service_account.Credentials.from_service_account_info(
        json.loads(credentials_info)
    )
    return build('drive', 'v3', credentials=credentials)

def download_file_from_drive(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh.read().decode('utf-8')

def get_drive_service():
    credentials_info = os.getenv("GOOGLE_CREDENTIALS")
    if not credentials_info:
        raise RuntimeError("GOOGLE_CREDENTIALS environment variable is not set")

    credentials = service_account.Credentials.from_service_account_info(
        json.loads(credentials_info)
    )
    return build("drive", "v3", credentials=credentials)

def upload_file(service, file_path, mime_type, parent_folder_id=None):
    file_metadata = {"name": os.path.basename(file_path)}
    if parent_folder_id:
        file_metadata["parents"] = [parent_folder_id]

    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get("id")

def list_files(service, folder_id=None):
    query = f"'{folder_id}' in parents" if folder_id else None
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get("files", [])

def delete_file(service, file_id):
    service.files().delete(fileId=file_id).execute()

def create_folder(service, folder_name, parent_folder_id=None):
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_folder_id:
        folder_metadata["parents"] = [parent_folder_id]

    folder = service.files().create(body=folder_metadata, fields="id").execute()
    return folder.get("id")
