from flask import Blueprint

cookbook_blueprint = Blueprint('cookbook', __name__)

from app.cookbook import cookbook_routes
