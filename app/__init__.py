#main app of the lidar server

from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)

from . import routes
