from flask import Flask, jsonify, request
import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import requests

app = Flask(__name__)

# Google Drive Service Initialization
def get_drive_service():
    credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
    credentials = Credentials.from_service_account_info(json.loads(credentials_json))
    return build('drive', 'v3', credentials=credentials)

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

    with open(file_name, 'w') as f:
        f.write(file_content)

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return jsonify({"file_id": file.get('id'), "message": "Schema uploaded to Google Drive."})

# Route: Download Schema from Google Drive
@app.route('/download-schema', methods=['GET'])
def download_schema():
    file_id = request.args.get('file_id')
    service = get_drive_service()

    request_drive = service.files().get_media(fileId=file_id)
    file_content = request_drive.execute()
    return jsonify({"schema": file_content.decode('utf-8')})

# Route: Push Schema to GitHub
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
    if response.status_code == 200:
        sha = response.json()['sha']
    else:
        sha = None

    # Push new file content
    file_content = request.json.get('content')
    encoded_content = file_content.encode('utf-8').decode('latin1')
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


#if __name__ == '__main__':
#    app.run(debug=True)
