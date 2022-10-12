import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import *
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    from blueprints.main import blueprint as api1
    app.register_blueprint(api1)
    return app