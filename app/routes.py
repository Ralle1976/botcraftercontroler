from flask import Blueprint, request, jsonify
from .github_api import get_user_info, list_repos, create_repo, delete_repo
from .gdrive_api import list_files, upload_file, delete_file

api = Blueprint('api', __name__)

# GitHub API Routen
@api.route('/github/user', methods=['GET'])
def github_user():
    return jsonify(get_user_info())

@api.route('/github/repos', methods=['GET'])
def github_repos():
    username = request.args.get('username')
    return jsonify(list_repos(username))

@api.route('/github/repo', methods=['POST'])
def github_create_repo():
    data = request.json
    return jsonify(create_repo(data['name'], data.get('private', True)))

@api.route('/github/repo', methods=['DELETE'])
def github_delete_repo():
    data = request.json
    return jsonify(delete_repo(data['owner'], data['repo']))

# Google Drive API Routen
@api.route('/gdrive/files', methods=['GET'])
def drive_files():
    return jsonify(list_files())

@api.route('/gdrive/upload', methods=['POST'])
def drive_upload():
    file = request.files['file']
    file_id = upload_file(file.filename, f"/tmp/{file.filename}", file.content_type)
    return jsonify({"file_id": file_id})

@api.route('/gdrive/delete', methods=['DELETE'])
def drive_delete():
    file_id = request.json['file_id']
    delete_file(file_id)
    return jsonify({"status": "deleted"})
