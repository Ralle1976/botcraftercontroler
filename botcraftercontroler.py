# BotCrafterController Erweiterung

from flask import Flask, request, jsonify
import os
import requests
import base64
from googleapiclient.discovery import build

app = Flask(__name__)

# Google Drive Service Initialisierung
def get_drive_service():
    # Hier wird angenommen, dass die Google API Credentials bereits konfiguriert sind.
    # Siehe: https://developers.google.com/drive/api/v3/quickstart/python
    return build('drive', 'v3')

# Route: Download Schema from Google Drive
@app.route('/download-schema', methods=['GET'])
def download_schema():
    file_id = request.args.get('file_id')
    service = get_drive_service()

    try:
        request_drive = service.files().get_media(fileId=file_id)
        file_content = request_drive.execute()
        return jsonify({"schema": file_content.decode('utf-8')})
    except Exception as e:
        return jsonify({"error": "Fehler beim Herunterladen des Schemas.", "details": str(e)}), 500

# Route: Push Schema to GitHub
@app.route('/push-schema', methods=['POST'])
def push_schema():
    repo = request.json.get('repo')
    token = request.json.get('token')
    file_path = request.json.get('file_path', 'schema.json')
    commit_message = request.json.get('message', 'Update schema')

    if not repo or not token:
        return jsonify({"error": "GitHub-Repository oder Token fehlt."}), 400

    headers = {
        'Authorization': f'token {token}'
    }

    # Fetch existing file content and SHA
    url = f'https://api.github.com/repos/{repo}/contents/{file_path}'
    response = requests.get(url, headers=headers)
    sha = response.json().get('sha') if response.status_code == 200 else None

    # Push new file content
    file_content = request.json.get('content')
    if not file_content:
        return jsonify({"error": "Kein Inhalt für das Schema bereitgestellt."}), 400

    encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
    data = {
        'message': commit_message,
        'content': encoded_content,
        'sha': sha
    }

    try:
        push_response = requests.put(url, headers=headers, json=data)
        if push_response.status_code in [200, 201]:
            return jsonify({"message": "Schema erfolgreich zu GitHub gepusht.", "details": push_response.json()})
        else:
            return jsonify({"error": "Fehler beim Pushen des Schemas.", "details": push_response.json()}), 400
    except Exception as e:
        return jsonify({"error": "Fehler beim Pushen des Schemas.", "details": str(e)}), 500

# Route: Liste aller verfügbaren Routen
@app.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({"route": rule.rule, "methods": list(rule.methods)})
    return jsonify({"available_routes": routes})

if __name__ == '__main__':
    app.run(debug=True)
