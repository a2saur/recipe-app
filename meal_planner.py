from config import Config

from app import create_app, db
from app.main.models import Recipe, RecipeIngredientUse, Ingredient, Tag, User, Certification
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'Recipe': Recipe, 'RecipeIngredientUse': RecipeIngredientUse, 'Ingredient': Ingredient, 'Tag': Tag, 'User': User}

@sqla.event.listens_for(Tag.__table__, 'after_create')
def add_tags(*args, **kwargs):
    query = sqla.select(Tag)
    if db.session.scalars(query).first() is None:
        tags = ['dinner', 'lunch', 'breakfast', 'snack', 'dessert', 'side', 'vegetarian', 
                'vegan', 'pescetarian', 'kosher', 'halal', 'gluten-free', 'easy', 'difficult', 
                'quick', 'oven', 'one-pot']
        for t in tags:
            db.session.add(Tag(name=t))
        db.session.commit()
        certifications = ['Certified Fundamental Cook', 'Certified Sous Chef', 'Certified Master Baker', 'Certified Working Pastry Chef',
                          "Retail Bakers of America", 'Certified Pastry Culinarian', 'Certified Foodservice Professional', 
                          'Master Certified Food Executive', 'Certified Chef de Cuisine', 'Certified Personal Chef', 'Certified Executive Chef',
                          'Certified Decorator', 'Certified Culinary Educator']

        for c in certifications:
            db.session.add(Certification(name=c))
        db.session.commit()

@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)