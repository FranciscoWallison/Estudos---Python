from flask import Blueprint
from flask_restx import Api
from namespaces.namespacesA import api as api1
from namespaces.namespacesB import api as api2

blueprint = Blueprint('main', __name__)

main = Api(blueprint)

main.add_namespace(api1)
main.add_namespace(api2)