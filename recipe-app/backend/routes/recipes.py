from flask import Blueprint, jsonify, request
from decimal import Decimal
from datetime import datetime
from models import (
    db,
    INGREDIENT_UNITS,
    Ingredient,
    Recipe,
    RecipeIngredientUse,
    RecipeStep,
)

recipes_bp = Blueprint("recipes", __name__)


@recipes_bp.get("/")
def get_recipes():
    recipes = (
        Recipe.query
        .filter_by(is_draft=False)
        .order_by(Recipe.timestamp.desc(), Recipe.id.desc())
        .all()
    )

    return jsonify([
        {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "serving_size": recipe.serving_size,
            "active_time": recipe.active_time,
            "overall_time": recipe.overall_time,
            "timestamp": (
                recipe.timestamp.isoformat()
                if recipe.timestamp else None
            ),
            "is_draft": recipe.is_draft,
            "to_make": recipe.to_make,
        }
        for recipe in recipes
    ]), 200


@recipes_bp.post("/")
def save_recipe():
    data = request.get_json(silent=True)
    if not data or not data.get("title", "").strip():
        return jsonify({"error": "Title is required"}), 400

    for item in data.get("ingredients", []):
        if item.get("unit", "") not in INGREDIENT_UNITS:
            return jsonify({
                "error": f"Invalid unit for {item.get('name', 'ingredient')}"
            }), 400

    recipe = Recipe(
        title=data["title"].strip(),
        description=data.get("description", ""),
        serving_size=data.get("serving_size", 1),
        active_time=data.get("active_time"),
        overall_time=data.get("overall_time"),
        is_draft=data.get("is_draft", True),
        to_make=data.get("to_make", False),
    )

    # Ingredients: reuse an existing Ingredient row by name, or create one.
    uses_by_name = {}
    for item in data.get("ingredients", []):
        name = item["name"].strip()
        ingredient = Ingredient.query.filter_by(name=name).first()
        if ingredient is None:
            ingredient = Ingredient(name=name)
            db.session.add(ingredient)

        use = RecipeIngredientUse(
            ingredient=ingredient,
            amount=Decimal(str(item["amount"])),
            unit=item.get("unit", ""),
        )
        recipe.ingredient_uses.append(use)
        uses_by_name[name.lower()] = use

    # Steps: link the first <ingredient> reference, since the model holds one.
    for step in data.get("steps", []):
        refs = step.get("ingredient_refs", [])
        recipe.steps.append(RecipeStep(
            step_number=step["step_number"],
            instruction=step["instruction"],
            ingredient_use=uses_by_name.get(refs[0].lower()) if refs else None,
        ))

    db.session.add(recipe)
    db.session.commit()

    return jsonify({"id": recipe.id}), 201



@recipes_bp.get("/<recipe_id>/view")
def view_recipe(recipe_id):
    recipe = db.session.get(Recipe, recipe_id)

    if not recipe:
        return jsonify({
            "error":"Recipe could not be found"
        }), 400
    if recipe.is_draft:
        return jsonify({
            "error":"Recipe is a draft and not viewable"
        }), 400

    return jsonify({
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "serving_size": recipe.serving_size,
            "active_time": recipe.active_time,
            "overall_time": recipe.overall_time,
            "timestamp": (
                datetime.strftime(recipe.timestamp, "%b %d %Y %H:%M")
                if recipe.timestamp else None
            ),
            "to_make": recipe.to_make,
            "ingredient_uses": [
                {
                    "id": use.id,
                    "ingredient_id": use.ingredient_id,
                    "name": use.ingredient.name,
                    "amount": float(use.amount),
                    "unit": use.unit,
                }
                for use in recipe.ingredient_uses
            ],
            "steps": [
                {
                    "id": step.id,
                    "step_number": step.step_number,
                    "instruction": step.instruction,
                    "ingredient_use_id": step.ingredient_use_id,
                }
                for step in recipe.steps
            ],
            "mode":"view"
        }), 200

