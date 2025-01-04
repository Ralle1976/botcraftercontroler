import os
import logging
import requests
import base64
import json
import base64 # Route: Push Schema to GitHub
from flask import Flask, jsonify, request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
#app.debug = True

# API-Token für die Autorisierung
API_TOKEN = os.getenv("API_TOKEN")


# Globale Debugging-Funktion
def log_request_details():
    headers = dict(request.headers)
    body = request.get_json(silent=True)
    args = request.args.to_dict()

    logger.info("Headers: %s", headers)
    logger.info("Body: %s", body)
    logger.info("Args: %s", args)

# Root-Route für die App
@app.route('/')
def index():
    return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.before_request
def before_request():
    log_request_details()  # Loggt alle Anfragen
    token = request.headers.get("Authorization")
    if token != API_TOKEN:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

# Google Drive Service Initialization
def get_drive_service():
    try:
        credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
        if not credentials_json:
            raise ValueError("GOOGLE_CREDENTIALS not set.")
        credentials = Credentials.from_service_account_info(json.loads(credentials_json))
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Google Drive service: {e}")


# Route: Upload Schema to Google Drive
@app.route('/upload-schema', methods=['POST'])
def upload_schema():
    file_content = request.json.get('content')
    file_name = request.json.get('name', 'schema.json')
    service = get_drive_service()

    file_metadata = {
        'name': file_name,
        'mimeType': 'application/json'
    }
    media = MediaFileUpload(file_name, mimetype='application/json', resumable=True)

    # Direkt-Upload
    file = service.files().create(body=file_metadata, media_body=MediaFileUpload(file_name, mimetype='application/json', resumable=False)).execute()
    return jsonify({"file_id": file.get('id'), "message": "Schema uploaded to Google Drive."})


# Route: Download Schema from Google Drive
@app.route('/download-schema', methods=['GET'])
def download_schema():
    file_id = request.args.get('file_id')
    service = get_drive_service()

    request_drive = service.files().get_media(fileId=file_id)
    file_content = request_drive.execute()
    return jsonify({"schema": file_content.decode('utf-8')})



@app.route('/push-schema', methods=['POST'])
def push_schema():
    repo = os.environ.get("GITHUB_REPO")
    token = os.environ.get("GITHUB_TOKEN")
    file_path = request.json.get('file_path', 'schema.json')
    commit_message = request.json.get('message', 'Update schema')

    headers = {
        'Authorization': f'token {token}'
    }

    # Fetch existing file content and SHA
    url = f'https://api.github.com/repos/{repo}/contents/{file_path}'
    response = requests.get(url, headers=headers)
    sha = response.json()['sha'] if response.status_code == 200 else None

    # Push new file content
    file_content = request.json.get('content')
    encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
    data = {
        'message': commit_message,
        'content': encoded_content,
        'sha': sha
    }

    push_response = requests.put(url, headers=headers, json=data)
    if push_response.status_code in [200, 201]:
        return jsonify({"message": "Schema pushed to GitHub.", "details": push_response.json()})
    else:
        return jsonify({"error": "Failed to push schema to GitHub.", "details": push_response.json()}), 400

@app.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({"route": rule.rule, "methods": list(rule.methods)})
    return jsonify({"available_routes": routes})


#if __name__ == '__main__':
#    app.run(debug=True)
