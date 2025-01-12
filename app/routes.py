from flask import Blueprint, request, jsonify
from .github_api import push_to_github
from .gdrive_api import get_drive_service, download_file_from_drive
from werkzeug.utils import quote as url_quote

api = Blueprint('api', __name__)



API_KEY = "API_TOKEN"

def check_auth(api_key):
    return api_key == API_KEY

@api.before_request
def authenticate():
    api_key = request.headers.get("X-API-KEY")
    if not check_auth(api_key):
        return jsonify({"error": "Nicht autorisiert"}), 401


@api.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Willkommen bei BotCrafterController!"})


# Route: Download Schema from Google Drive
@api.route('/download-schema', methods=['GET'])
def download_schema():
    file_id = request.args.get('file_id')
    service = get_drive_service()

    try:
        file_content = download_file_from_drive(service, file_id)
        return jsonify({"schema": file_content})
    except Exception as e:
        return jsonify({"error": "Fehler beim Herunterladen des Schemas.", "details": str(e)}), 500

# Route: Push Schema to GitHub
@api.route('/push-schema', methods=['POST'])
def push_schema():
    repo = request.json.get('repo')
    token = request.json.get('token')
    file_path = request.json.get('file_path', 'schema.json')
    commit_message = request.json.get('message', 'Update schema')
    file_content = request.json.get('content')

    if not repo or not token or not file_content:
        return jsonify({"error": "Fehlende Eingaben: repo, token oder content"}), 400

    try:
        push_response = push_to_github(repo, token, file_path, commit_message, file_content)
        if push_response.status_code in [200, 201]:
            return jsonify({"message": "Schema erfolgreich zu GitHub gepusht.", "details": push_response.json()})
        else:
            return jsonify({"error": "Fehler beim Pushen des Schemas.", "details": push_response.json()}), 400
    except Exception as e:
        return jsonify({"error": "Fehler beim Pushen des Schemas.", "details": str(e)}), 500

# Route: Liste aller verfügbaren Routen
@api.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in api.url_map.iter_rules():
        routes.append({"route": rule.rule, "methods": list(rule.methods)})
    return jsonify({"available_routes": routes})

@api.route("/list-repos", methods=["GET"])
def list_repos():
    """
    Gibt die verfügbaren Repositories zurück, ohne die Tokens offenzulegen.
    """
    repos = Config.list_repos()
    # Rückgabe der Repos ohne sensible Daten
    repo_details = [
        {"name": repo_name, "url": Config.get_repo_config(repo_name)["url"]}
        for repo_name in repos
    ]
    return jsonify({"repositories": repo_details})


@api.route("/repo-contents", methods=["GET"])
def repo_contents():
    """
    Gibt die Inhalte eines Repositories zurück, basierend auf dem Namen und einem optionalen Pfad.
    Query-Parameter:
      - repo_name: Name des Repositories in der Konfiguration.
      - path (optional): Der spezifische Pfad im Repository.
    """
    repo_name = request.args.get("repo_name")
    path = request.args.get("path", "")

    if not repo_name:
        return jsonify({"error": "Parameter 'repo_name' ist erforderlich"}), 400

    repo_config = Config.get_repo_config(repo_name)
    if not repo_config:
        return jsonify({"error": f"Repository '{repo_name}' nicht gefunden"}), 404

    try:
        # Abrufen der Repository-Inhalte
        token = repo_config.get("token")
        url = repo_config.get("url")
        headers = {"Authorization": f"token {token}"}
        api_url = f"https://api.github.com/repos/{'/'.join(url.split('/')[-2:])}/contents/{path}"
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": response.json(), "status_code": response.status_code}), 400
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Inhalte: {str(e)}"}), 500
