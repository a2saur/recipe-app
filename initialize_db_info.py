from app import create_app, db
from config import Config
from datetime import datetime, timezone

app = create_app(Config)

from app.main.models import Recipe, Cookbook, User, Ingredient, Tag, RecipeIngredientUse
from config  import Config

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
import os

if os.path.exists("meal_planner.db"):
    os.remove("meal_planner.db")

app.app_context().push()

db.create_all()

# ----- Add Users -----
u1 = User(
    first_name = "A",
    last_name = "S",
    username = "A2",
    email = "a@wpi.edu",
)
u1.set_password("123")
db.session.add(u1)

u2 = User(
    first_name = "Mama",
    last_name = "Nintendo",
    username = "CookingMama",
    email = "cooking@nintendo.com",
)
u2.set_password("123")
db.session.add(u2)

u3 = User(
    first_name = "Mama",
    last_name = "Nintendo",
    username = "CookingMama",
    email = "cooking@nintendo.com",
)
u3.set_password("123")
db.session.add(u3)

db.session.commit()

# --- Add ingredients ---
i1 = Ingredient(name="chicken")
db.session.add(i1)
i2 = Ingredient(name="zucchini")
db.session.add(i2)
i3 = Ingredient(name="rice")
db.session.add(i3)

db.session.commit()


# --- Add Tags ---
tagsToAdd = ["dinner", "lunch", "breakfast", 
             "snack", "dessert", 
             "vegetarian", "vegan", "pescetarian", 
             "kosher", "halal",
             "gluten free",
             "easy", "difficult"]
for tName in tagsToAdd:
    t1 = Tag(name=tName)
    db.session.add(t1)
    db.session.commit()


# --- Add recipe ---
r1 = Recipe(
    title = "Chicken and Rice",
    description = "This recipe is for an easy dinner - chicken with rice",
    servingSize = 2,
    estimatedHrs = 0,
    estimatedMins = 45,
    # steps = "1. Wash rice 2. Cook rice 3. Cook chicken",
    is_draft=False,
    user_id=u1.id
)
r1.tags.add(db.session.scalars(sqla.select(Tag).where(Tag.name == "dinner")).first())
r1.timestamp = datetime.now(timezone.utc)
r1.pictFile = "8fc7b56a-0c16-11f1-99cc-1ebf2a7aaad6_blue-pikmin.png"
db.session.add(r1)

r2 = Recipe(
    title = "Simple Garlic Butter Eggs & Toast",
    description = "A quick, comforting breakfast made with soft scrambled eggs cooked in garlic butter and served over warm toast.",
    servingSize = 1,
    estimatedHrs = 0,
    estimatedMins = 10,
    # steps = "1. Toast the Bread 2. Beat the Eggs 3. Cook the Eggs 4. Serve",
    is_draft=False,
    user_id=u1.id
)
r2.tags.add(db.session.scalars(sqla.select(Tag).where(Tag.name == "easy")).first())
r2.timestamp = datetime.now(timezone.utc)
r2.pictFile = "hq720.jpg"
db.session.add(r2)

db.session.commit()


# --- Add recipe ingredients ---
ri1 = RecipeIngredientUse(
    recipe_id = r1.id,
    ingredient_id = i2.id,
    amount = 1,
    unit = "lb"
)
db.session.add(ri1)


# --- Add cookbooks ---
c1 = Cookbook()