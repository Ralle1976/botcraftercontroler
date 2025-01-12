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

def create_repository(token, repo_name, private=True):
    headers = {"Authorization": f"token {token}"}
    data = {"name": repo_name, "private": private}
    response = requests.post(f"{GITHUB_API_URL}/user/repos", headers=headers, json=data)
    return response.json()

def list_files_in_repo(token, owner, repo, path=""):
    headers = {"Authorization": f"token {token}"}
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=headers)
    return response.json()

def delete_file(token, owner, repo, path, sha):
    headers = {"Authorization": f"token {token}"}
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}"
    data = {"message": f"Deleting {path}", "sha": sha}
    response = requests.delete(url, headers=headers, json=data)
    return response.json()

def create_branch(token, owner, repo, branch_name, source_branch="main"):
    headers = {"Authorization": f"token {token}"}
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/refs/heads/{source_branch}"
    source_ref = requests.get(url, headers=headers).json()
    sha = source_ref.get("object", {}).get("sha")
    data = {"ref": f"refs/heads/{branch_name}", "sha": sha}
    response = requests.post(f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/refs", headers=headers, json=data)
    return response.json()

def create_pull_request(token, owner, repo, title, head, base):
    headers = {"Authorization": f"token {token}"}
    data = {"title": title, "head": head, "base": base}
    response = requests.post(f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls", headers=headers, json=data)
    return response.json()
