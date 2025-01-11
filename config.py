import os

class Config:
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', 'your_github_token')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'your_google_client_id')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'your_google_client_secret')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
