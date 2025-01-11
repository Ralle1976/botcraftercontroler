import os
import requests
import base64

GITHUB_API_URL = "https://api.github.com"

def push_to_github(repo, token, file_path, commit_message, file_content):
    headers = {
        'Authorization': f'token {token}'
    }
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{file_path}"

    # Prüfen, ob die Datei existiert, um SHA zu erhalten
    response = requests.get(url, headers=headers)
    sha = response.json().get('sha') if response.status_code == 200 else None

    encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
    data = {
        'message': commit_message,
        'content': encoded_content,
        'sha': sha
    }

    push_response = requests.put(url, headers=headers, json=data)
    return push_response
