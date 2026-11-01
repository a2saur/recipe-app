from flask import Blueprint, jsonify, request
from decimal import Decimal, InvalidOperation
from datetime import date
from models import (
    db,
    GROCERY_LOCATIONS,
    INGREDIENT_UNITS,
    GroceryListItem,
    Ingredient,
    OwnedGrocery,
)

groceries_bp = Blueprint("groceries", __name__)


def serialize_owned(grocery):
    return {
        "id": grocery.id,
        "ingredient_id": grocery.ingredient_id,
        "name": grocery.ingredient.name,
        "amount": float(grocery.amount),
        "unit": grocery.unit,
        "location": grocery.location,
        "expiration_date": (
            grocery.expiration_date.isoformat()
            if grocery.expiration_date else None
        ),
        "is_hard_expiration": grocery.is_hard_expiration,
    }


def serialize_list_item(item):
    return {
        "id": item.id,
        "ingredient_id": item.ingredient_id,
        "name": item.ingredient.name,
        "amount": float(item.amount),
        "unit": item.unit,
        "is_checked": item.is_checked,
    }


def parse_ingredient_fields(data):
    """Validate name/amount/unit; returns (fields, error message)."""
    name = (data.get("name") or "").strip()
    if not name:
        return None, "Ingredient name is required"

    try:
        amount = Decimal(str(data.get("amount", 1)))
    except InvalidOperation:
        return None, "Amount must be a number"
    if not amount.is_finite() or amount <= 0:
        return None, "Amount must be greater than zero"

    unit = data.get("unit", "")
    if unit not in INGREDIENT_UNITS:
        return None, f"Invalid unit for {name}"

    # Reuse an existing Ingredient row by name, or create one.
    ingredient = Ingredient.query.filter_by(name=name).first()
    if ingredient is None:
        ingredient = Ingredient(name=name)
        db.session.add(ingredient)

    return {"ingredient": ingredient, "amount": amount, "unit": unit}, None


@groceries_bp.get("/")
def get_groceries():
    owned = (
        OwnedGrocery.query
        .order_by(
            OwnedGrocery.expiration_date.is_(None),
            OwnedGrocery.expiration_date,
            OwnedGrocery.id,
        )
        .all()
    )
    list_items = (
        GroceryListItem.query
        .order_by(GroceryListItem.is_checked, GroceryListItem.id)
        .all()
    )

    return jsonify({
        "owned": [serialize_owned(grocery) for grocery in owned],
        "list": [serialize_list_item(item) for item in list_items],
    }), 200


# ------------------------------------------------------------
# Owned groceries
# ------------------------------------------------------------

@groceries_bp.post("/owned")
def add_owned_grocery():
    data = request.get_json(silent=True) or {}

    fields, error = parse_ingredient_fields(data)
    if error:
        return jsonify({"error": error}), 400

    location = data.get("location")
    if location not in GROCERY_LOCATIONS:
        return jsonify({"error": "Invalid location"}), 400

    expiration_date = None
    if data.get("expiration_date"):
        try:
            expiration_date = date.fromisoformat(data["expiration_date"])
        except ValueError:
            return jsonify({"error": "Invalid expiration date"}), 400

    grocery = OwnedGrocery(
        **fields,
        location=location,
        expiration_date=expiration_date,
        is_hard_expiration=bool(data.get("is_hard_expiration", False)),
    )
    db.session.add(grocery)
    db.session.commit()

    return jsonify(serialize_owned(grocery)), 201


@groceries_bp.delete("/owned/<int:grocery_id>")
def delete_owned_grocery(grocery_id):
    grocery = db.session.get(OwnedGrocery, grocery_id)
    if not grocery:
        return jsonify({"error": "Grocery could not be found"}), 404

    db.session.delete(grocery)
    db.session.commit()

    return "", 204


# ------------------------------------------------------------
# Grocery list
# ------------------------------------------------------------

@groceries_bp.post("/list")
def add_list_item():
    data = request.get_json(silent=True) or {}

    fields, error = parse_ingredient_fields(data)
    if error:
        return jsonify({"error": error}), 400

    item = GroceryListItem(**fields)
    db.session.add(item)
    db.session.commit()

    return jsonify(serialize_list_item(item)), 201


@groceries_bp.patch("/list/<int:item_id>")
def update_list_item(item_id):
    item = db.session.get(GroceryListItem, item_id)
    if not item:
        return jsonify({"error": "List item could not be found"}), 404

    data = request.get_json(silent=True) or {}
    if "is_checked" in data:
        item.is_checked = bool(data["is_checked"])
    db.session.commit()

    return jsonify(serialize_list_item(item)), 200


@groceries_bp.delete("/list/<int:item_id>")
def delete_list_item(item_id):
    item = db.session.get(GroceryListItem, item_id)
    if not item:
        return jsonify({"error": "List item could not be found"}), 404

    db.session.delete(item)
    db.session.commit()

    return "", 204
