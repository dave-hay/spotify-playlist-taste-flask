from pathlib import Path
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app._static_folder = Path('/Users/davidhay/PycharmProjects/spotify-music-taste-flask/app/static')

from app import routes
