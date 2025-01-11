import os

class Config:
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', 'default_github_token')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'default_google_client_id')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'default_google_client_secret')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
