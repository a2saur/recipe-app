from sqlalchemy import func
from app import db
from app.main.models import Recipe, RecipeIngredientUse, UserIngredientListUse

def get_recommended_recipes(user_id):

    match_score = (
        func.count(UserIngredientListUse.ingredient_id) * 1.0 / func.count(RecipeIngredientUse.ingredient_id)
    ).label("match_score")
    results = db.session.query(Recipe, match_score).join(RecipeIngredientUse, Recipe.id == RecipeIngredientUse.recipe_id).outerjoin(
                                    UserIngredientListUse, (UserIngredientListUse.ingredient_id == RecipeIngredientUse.ingredient_id) & (
                                        UserIngredientListUse.user_id == user_id
                                    )
                                ).group_by(Recipe.id).order_by(match_score.desc()).limit(7).all()
    
    return [row[0] for row in results]
