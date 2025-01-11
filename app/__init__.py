from flask import Flask
from .routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(api, url_prefix='/')  # Blueprint für die Haupt-URL registrieren
    return app
