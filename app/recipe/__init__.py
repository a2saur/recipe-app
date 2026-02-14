from flask import Blueprint

recipe_blueprint = Blueprint('recipe', __name__)

from app.recipe import recipe_routes
