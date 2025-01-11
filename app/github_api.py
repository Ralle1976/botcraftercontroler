import os
import requests

GITHUB_API_URL = "https://api.github.com"
TOKEN = os.getenv('GITHUB_TOKEN')

def make_github_request(endpoint, method="GET", payload=None, params=None):
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{GITHUB_API_URL}{endpoint}"
    response = requests.request(method, url, headers=headers, json=payload, params=params)
    response.raise_for_status()
    return response.json()

def get_user_info():
    return make_github_request("/user")

def list_repos(username):
    return make_github_request(f"/users/{username}/repos")

def create_repo(repo_name, private=True):
    payload = {"name": repo_name, "private": private}
    return make_github_request("/user/repos", method="POST", payload=payload)

def delete_repo(owner, repo):
    return make_github_request(f"/repos/{owner}/{repo}", method="DELETE")
