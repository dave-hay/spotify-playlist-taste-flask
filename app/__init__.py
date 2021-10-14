from pathlib import Path
from flask import Flask
from config import Config

app = Flask(__name__, static_folder=Path.cwd()/'app/static')
app.config.from_object(Config)

from app import routes
