import os

from flask import (Flask, request)
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from exif import Image
import reverse_geocoder as rg
import pycountry

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "\\images\\"

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import images
    app.register_blueprint(images.bp)
    
    from . import dynamodb_handler
    app.register_blueprint(dynamodb_handler.bp)
    
    from . import db
    db.init_app(app)

    return app

