from sqlalchemy import func
from app import db
from app.main.models import Recipe, RecipeIngredientUse, UserIngredientListUse
from app.main.models import recipe_tags_table, user_preferred_tags, Tag

def get_recommended_recipes(user_id):
    ingredient_match = (
        func.count(UserIngredientListUse.ingredient_id) * 1.0 / 
        func.nullif(func.count(RecipeIngredientUse.ingredient_id), 0)
    )

    tags_match = (
        func.count(user_preferred_tags.c.tag_id) * 1.0 
    )

    total_score = (ingredient_match + tags_match).label("match_score")

    results = db.session.query(Recipe, total_score)\
        .join(RecipeIngredientUse, Recipe.id == RecipeIngredientUse.recipe_id)\
        .outerjoin(UserIngredientListUse, 
            (UserIngredientListUse.ingredient_id == RecipeIngredientUse.ingredient_id) & 
            (UserIngredientListUse.user_id == user_id)
        )\
        .outerjoin(recipe_tags_table, Recipe.id == recipe_tags_table.c.recipe_id)\
        .outerjoin(user_preferred_tags, 
            (user_preferred_tags.c.tag_id == recipe_tags_table.c.tag_id) & 
            (user_preferred_tags.c.user_id == user_id)
        )\
        .group_by(Recipe.id)\
        .order_by(total_score.desc())\
        .limit(6).all()
    
    return [row[0] for row in results]
