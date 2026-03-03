from sqlalchemy import func, select, and_
from app import db
from app.main.models import Recipe, RecipeIngredientUse, UserIngredientListUse
from app.main.models import recipe_tags_table, user_preferred_tags, Tag, user_allergies, user_dietary_tags

def get_recommended_recipes(user_id):
    # Hard filter the allergies; exclude recipes with allergic ingredients
    allergic_recipes = select(RecipeIngredientUse.recipe_id).join(
        user_allergies, RecipeIngredientUse.ingredient_id == user_allergies.c.ingredient_id
    ).where(user_allergies.c.user_id == user_id)

    # Hard filter the dietary tags; recipe must have all tags the user is restricted to
    user_restrictions = db.session.scalars(
        select(user_dietary_tags.c.tag_id).where(user_dietary_tags.c.user_id == user_id)
    ).all()

    # Match scoring
    ingredient_match = (
        func.count(UserIngredientListUse.ingredient_id) * 1.0 / 
        func.nullif(func.count(RecipeIngredientUse.ingredient_id), 0)
    )

    tags_match = (
        func.count(user_preferred_tags.c.tag_id) * 1.0 
    )

    total_score = (ingredient_match + tags_match).label("match_score")


    query = db.session.query(Recipe, total_score)\
        .join(RecipeIngredientUse, Recipe.id == RecipeIngredientUse.recipe_id)\
        .outerjoin(UserIngredientListUse, 
            (UserIngredientListUse.ingredient_id == RecipeIngredientUse.ingredient_id) & 
            (UserIngredientListUse.user_id == user_id)
        )\
        .outerjoin(recipe_tags_table, Recipe.id == recipe_tags_table.c.recipe_id)\
        .outerjoin(user_preferred_tags, 
            (user_preferred_tags.c.tag_id == recipe_tags_table.c.tag_id) & 
            (user_preferred_tags.c.user_id == user_id)
        )
    
    query = query.filter(~Recipe.id.in_(allergic_recipes))

    if user_restrictions:
        for tag_id in user_restrictions:
            query = query.filter(Recipe.id.in_(
                select(recipe_tags_table.c.recipe_id).where(recipe_tags_table.c.tag_id == tag_id)
            ))
    
    results = query.group_by(Recipe.id).order_by(total_score.desc()).limit(6)
    
    return [row[0] for row in results]