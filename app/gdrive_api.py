from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

def get_drive_service():
    # Hier wird angenommen, dass die Google API Credentials bereits konfiguriert sind.
    # Siehe: https://developers.google.com/drive/api/v3/quickstart/python
    return build('drive', 'v3')

def download_file_from_drive(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh.read().decode('utf-8')
