from app import create_app, db
from config import Config

app = create_app(Config)

from app.main.models import Recipe, Cookbook, User
from config  import Config

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
import os

# if os.path.exists("mealplanner.db"):
#     os.remove("mealplanner.db")

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