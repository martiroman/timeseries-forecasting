from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()  # .env

def create_service():
    app = Flask(__name__)

    app.config['PROMETHEUS_URL'] = os.getenv('PROMETHEUS_URL')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
