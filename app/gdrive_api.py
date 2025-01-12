import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
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
