from flask import Blueprint

user_blueprint = Blueprint('user', __name__)

from app.user import user_routes
