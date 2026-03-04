"""
This file contains the functional tests for the main.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
from datetime import date, datetime
import os
from turtle import title
from time import timezone
from datetime import datetime, UTC
import pytest
from app import create_app, db
from app.main.models import Ingredient, User, Tag, Recipe, RecipeIngredientUse, RecipeStep, Recipe, Cookbook, RecipeIngredientUse, UserIngredientListUse, UserGroceryListUse, RecipeStep, Certification, UserCertification, IngredientCostEntry
from config import Config
import sqlalchemy as sqla
from datetime import datetime, timezone
import io


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True



@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

def new_user(first_name, last_name, username, email, password, 
             certified=True, allergies=None, dietary_tags=None, preferred_tags=None):

    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        is_certified = certified,
        )
    user.set_password(password)

    # Add allergies (expecting a list of Ingredient objects)
    if allergies:
        for ingredient in allergies:
            user.allergies.add(ingredient)

    # Add dietary tags (expecting a list of Tag objects)
    if dietary_tags:
        for tag in dietary_tags:
            user.dietary_tags.add(tag)

    # Add preferred tags (expecting a list of Tag objects)
    if preferred_tags:
        for tag in preferred_tags:
            user.preferred_tags.add(tag)

    return user

def new_recipe(title, description, servingSize, estimatedHrs, estimatedMins, timestamp, is_draft, user_id, save_count=0, pictFile=None):
    recipe = Recipe(
        title=title,
        pictFile=pictFile,
        description=description,
        servingSize=servingSize,
        estimatedHrs=estimatedHrs,
        estimatedMins=estimatedMins,
        timestamp=timestamp,
        is_draft=is_draft,
        user_id=user_id,
        save_count=save_count
    )
    return recipe

def new_recipe_ingredient_use(recipe_id, ingredient_id, amount, unit):
    recipe_ingredient_use = RecipeIngredientUse(
        recipe_id=recipe_id,
        ingredient_id=ingredient_id,
        amount=amount,
        unit=unit
    )
    return recipe_ingredient_use

def init_ingredients():
    ingredients = ['Peanuts', 'Shrimp', 'Milk', 'Eggs', 'Wheat', 'Soy', 'Onion',
                    'Cream', 'Corn', 'Butter', 'Garlic', 'Tomato', 'Chicken', 'Beef', 
                    'Pork', 'Fish', 'Shellfish', 'Rice', 'Potato', 'Carrot', 'Bell Pepper', 
                    'Bread', 'Flour', 'Sugar', 'Salt', 'Pepper', 'Pasta', 'Parmesan', 'Avocado', 
                    'Scallions', 'Chilis', 'Lettuce', 'Dressing', 'Tomatoes', 'Dried Fruits']
    for name in ingredients:
        exists = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == name)).first()
        if not exists:
            db.session.add(Ingredient(name=name))
    db.session.commit()
    return None

def init_tags():
    # check if any tags are already defined in the database
    count = db.session.scalar(db.select(db.func.count(Tag.id)))
    print("**************", count)
    # initialize the tags
    if count == 0:
        tags = ['dinner', 'lunch', 'breakfast', 'snack', 'dessert', 'side', 'vegetarian', 
                'vegan', 'pescetarian', 'kosher', 'halal', 'gluten-free', 'easy', 'difficult', 
                'quick', 'oven', 'one-pot']
        for t in tags:
            db.session.add(Tag(name=t))
        db.session.commit()
    return None

@pytest.fixture
def init_database():
    db.session.remove()
    db.drop_all()

    # Create the database and the database table
    db.create_all()
    # initialize the tags & ingredients
    init_tags()
    init_ingredients()

    # Fetch the tags to use for the tests
    vegan_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first()
    easy_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'easy')).first()
    breakfast_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'breakfast')).first()
    
    # Create an allergy ingredient object
    peanut_allergy = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Peanuts')).first()

    # Add a user    
    user1 = new_user(first_name='Cooking', last_name='Mama', username='CookingMama', email='cookingmama@wpi.edu', password='123',
                     certified=True, allergies=[peanut_allergy], dietary_tags=[vegan_tag], preferred_tags=[easy_tag, breakfast_tag])
    # Insert user data
    db.session.add(user1)
    # Add a user    
    user2 = new_user(first_name='Not', last_name='Certified', username='notcertified', email='a@wpi.edu', password='123',
                     certified=False, allergies=[], dietary_tags=[], preferred_tags=[breakfast_tag])
    # Insert user data
    db.session.add(user2)

    # Add a recipe for the user

    # Commit the changes for the users
    db.session.commit()

    # add a couple ingredients
    i1 = Ingredient(name="avocado")
    db.session.add(i1)
    i2 = Ingredient(name="bread")
    db.session.add(i2)
    db.session.commit()

    # add a recipe
    r1 = Recipe(title = "Avocado Sandwich", description = "A delicious and easy breakfast", servingSize = 1, estimatedHrs = 0, estimatedMins = 15, is_draft=False, user_id=user1.id)
    r1.timestamp = datetime.now(timezone.utc)
    db.session.add(r1)
    db.session.commit()

    # add ingredient uses to recipe
    r1i1 = RecipeIngredientUse(recipe_id=r1.id, ingredient_id=i1.id, amount=1, unit="unit")
    db.session.add(r1i1)
    r1i2 = RecipeIngredientUse(recipe_id=r1.id, ingredient_id=i2.id, amount=2, unit="unit")
    db.session.add(r1i2)
    db.session.commit()

    yield db  # this is where the testing happens!

    db.session.remove()
    db.drop_all()

# ------------------------------------
# AUTH ROUTES TESTS

def test_register_page(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/user/register')
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Choose user type" in response.data

def test_register_regular_user(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Get tags for dietary restrictions and preferred tags
    vegan_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first()
    easy_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'easy')).first()

    # Create a test client using the Flask application configured for testing
    response = test_client.post('/user/register', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'john@wpi.edu',
        'password': "bad-bad-password",
        'password2': "bad-bad-password",
        'user_type': 'regular',
        'allergies-0-ingredientName': 'Peanuts',
        'allergies-1-ingredientName': 'Shrimp',
        'dietary_restrictions': [vegan_tag.id],
        'tags': [easy_tag.id]
    }, follow_redirects = True)
    assert response.status_code == 200
    
    # Verify that the user was added to the database with the correct information
    user = db.session.scalars(sqla.select(User).where(User.username == 'johndoe')).first()
    user_count = db.session.scalar(sqla.select(db.func.count()).where(User.username == 'johndoe'))
    assert user.email == 'john@wpi.edu'
    assert user_count == 1

    # Verify that the user's allergies were added to the database
    allergies = db.session.scalars(user.allergies.select()).all()
    peanuts = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Peanuts')).first()
    assert peanuts in allergies

    # Verify that the user's dietary restrictions were added to the database
    dietary_tag = db.session.scalars(user.dietary_tags.select()).all()
    assert vegan_tag in dietary_tag

    # Verify that the user's preferred tags were added to the database
    preferred_tag = db.session.scalars(user.preferred_tags.select()).all()
    assert easy_tag in preferred_tag

    assert b"Sign In" in response.data   
    
def test_register_certified_user_redirection(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted with user_type='certified'
    THEN check that the user is redirected to the certification page
    """
    # Get a tag to use for the form
    vegan_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first()

    # Submit the form as a certified user
    response = test_client.post('/user/register', data={
        'first_name': 'Sunny',
        'last_name': 'Kang',
        'username': 'sunnykang',
        'email': 'skang1@wpi.edu',
        'password': 'password123',
        'password2': 'password123',
        'user_type': 'certified',  # This triggers the redirect logic
        'dietary_restrictions': [vegan_tag.id]
    }, follow_redirects=False) # We want to check the redirect itself

    # 1. Check for the 302 Redirect status code
    assert response.status_code == 302
    
    # 2. Verify it points to the correct location
    # This checks if the 'Location' header contains the become_certified route
    assert '/user/profile/certify' in response.headers['Location']

    # 3. Verify Session data
    # You can access the session via the test_client context
    with test_client.session_transaction() as sess:
        assert sess.get('from_reg') is True
        assert sess.get('reg_email') == 'skang1@wpi.edu'

def test_invalidlogin(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/user/login', 
                          data=dict(username='snow', password='12345',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

# ------------------------------------
# Helper functions

def do_login(test_client, path , username, passwd):
    response = test_client.post(path, 
                          data=dict(username= username, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    #Students should update this assertion condition according to their own page content
    assert b"Welcome!" in response.data  

def do_logout(test_client, path):
    response = test_client.get(path,                       
                          follow_redirects = True)
    assert response.status_code == 200
    # Assuming the application re-directs to login page after logout.
    #Students should update this assertion condition according to their own page content 
    assert b"Sign In" in response.data
    assert b"Click to Register!" in response.data    
# ------------------------------------

def test_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    do_logout(test_client, path = '/user/logout')

# ------------------------------------
# MAIN ROUTES TESTS

# Helper functions
def add_recipe_posts(test_client, init_database):
    # Post three recipes with different tags and check that they are recommended correctly based on the user's preferred tags and dietary restrictions
    pictFile0 = "207add98-112c-11f1-a181-1ebf2a7aaad6_cooking-mama-corn-potage.png"
    r0 = new_recipe(title = "Corn Soup", description = "Known in Japan as \"corn potage\", this recipe is made from corn kernels cut from the cob. The soup becomes very smooth and strained after cooking, creating a thick paste-like texture, similar to seafood bisque.", 
                    servingSize = 1, estimatedHrs = 0, estimatedMins = 45, timestamp=datetime(2026, 1, 1, 10, 30, tzinfo=UTC), is_draft=False, user_id=0, save_count=4, pictFile = pictFile0)
    db.session.add(r0)

    pictFile1 = "2b117cbc-112c-11f1-a181-1ebf2a7aaad6_cooking-mama-avocado-toast.png"
    r1 = new_recipe(title = "Avocado Toast", description = "Guacamole spread topped with chilis!", 
                    servingSize = 1, estimatedHrs = 0, estimatedMins = 15, timestamp=datetime(2026, 1, 1, 10, 40, tzinfo=UTC), is_draft=False, user_id=0, save_count=5, pictFile = pictFile1)
    db.session.add(r1)

    r2 = new_recipe(title = "Tomato Salad", description = "Lettuce and tomato salad!", 
                    servingSize = 1, estimatedHrs = 0, estimatedMins = 15, timestamp=datetime(2026, 1, 1, 10, 50, tzinfo=UTC), is_draft=False, user_id=0, save_count=3)
    db.session.add(r2)

    r3 = new_recipe(title = "Avocado Salad", description = "Lettuce and avocado salad!", 
                    servingSize = 1, estimatedHrs = 0, estimatedMins = 15, timestamp=datetime(2026, 1, 2, 11, 0, tzinfo=UTC), is_draft=False, user_id=0, save_count=2)
    db.session.add(r3)

    r4 = new_recipe(title = "Trail Mix", description = "A mix of nuts and dried fruits!", 
                    servingSize = 1, estimatedHrs = 0, estimatedMins = 5, timestamp=datetime(2026, 1, 2, 11, 10, tzinfo=UTC), is_draft=False, user_id=0, save_count=0)
    db.session.add(r4)
    db.session.commit()

    # Get tags 
    vegan_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first()

    # Get user's preferred tags
    easy_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'easy')).first()
    breakfast_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'breakfast')).first()

    # Add tags to the recipes
    r0.tags.add(easy_tag) # Corn Soup is easy but not vegan, so it should not be recommended based on CookingMama's preferences

    r1.tags.add(vegan_tag) # Avocado Toast is vegan, so it should be recommended based on CookingMama's preferences
    r1.tags.add(easy_tag) # Avocado Toast is easy, so it should be recommended based on CookingMama's preferences
    r1.tags.add(breakfast_tag) # Avocado Toast is a breakfast recipe, so it should be recommended based on CookingMama's preferences
    
    r2.tags.add(vegan_tag) # Tomato Salad is vegan, so it should be recommended based on CookingMama's preferences
    r2.tags.add(easy_tag) # Tomato Salad is easy, so it should be recommended based on CookingMama's preferences

    r3.tags.add(vegan_tag) # Avocado Salad is vegan, so it should be recommended based on CookingMama's preferences
    r3.tags.add(easy_tag) # Avocado Salad is easy, so it should be recommended based on CookingMama's preferences

    r4.tags.add(vegan_tag) # Trail Mix is vegan, so it should be recommended based on CookingMama's preferences
    r4.tags.add(easy_tag) # Trail Mix is easy, so it should be recommended based on CookingMama's preferences
    db.session.commit()

    # Add ingredients to the recipe
    onion = new_recipe_ingredient_use(recipe_id = r0.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Onion')).first().id, amount = 0.5, unit = "unit")
    db.session.add(onion)
    cream = new_recipe_ingredient_use(recipe_id = r0.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Cream')).first().id, amount = 1, unit = "cup")
    db.session.add(cream)
    corn = new_recipe_ingredient_use(recipe_id = r0.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Corn')).first().id, amount = 4, unit = "tbsp")
    db.session.add(corn)
    avocado = new_recipe_ingredient_use(recipe_id = r1.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Avocado')).first().id, amount = 1, unit = "unit")
    db.session.add(avocado)
    scallions = new_recipe_ingredient_use(recipe_id = r1.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Scallions')).first().id, amount = 2, unit = "tbsp")
    db.session.add(scallions)
    chilis = new_recipe_ingredient_use(recipe_id = r1.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Chilis')).first().id, amount = 1, unit = "tbsp")
    db.session.add(chilis)
    lettuce = new_recipe_ingredient_use(recipe_id = r2.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Lettuce')).first().id, amount = 1, unit = "unit")
    db.session.add(lettuce)
    tomatoes = new_recipe_ingredient_use(recipe_id = r2.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Tomatoes')).first().id, amount = 1, unit = "cup")
    db.session.add(tomatoes)
    dressing = new_recipe_ingredient_use(recipe_id = r2.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Dressing')).first().id, amount = 2, unit = "tbsp")
    db.session.add(dressing)
    lettuce2 = new_recipe_ingredient_use(recipe_id = r3.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Lettuce')).first().id, amount = 1, unit = "unit")
    db.session.add(lettuce2)
    avocado2 = new_recipe_ingredient_use(recipe_id = r3.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Avocado')).first().id, amount = 1, unit = "unit")
    db.session.add(avocado2)
    dressing2 = new_recipe_ingredient_use(recipe_id = r3.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Dressing')).first().id, amount = 2, unit = "tbsp")
    db.session.add(dressing2)
    peanuts = new_recipe_ingredient_use(recipe_id = r4.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Peanuts')).first().id, amount = 0.5, unit = "cup")
    db.session.add(peanuts)
    dried_fruits = new_recipe_ingredient_use(recipe_id = r4.id, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Dried Fruits')).first().id, amount = 0.5, unit = "cup")
    db.session.add(dried_fruits)


def test_recommended_recipes(test_client,init_database): # rewrite this test
    """
    GIVEN a Flask application configured for testing , after user logs-in,
    THEN check that response is valid and the recommended recipes are updated in the database
    """
    # Login as CookingMama
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    add_recipe_posts(test_client, init_database)

    # Add user's current ingredients
    letture_ing = UserIngredientListUse(user_id = 1, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Lettuce')).first().id, amount = 1, unit = "unit")
    avocado_ing = UserIngredientListUse(user_id = 1, ingredient_id = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == 'Avocado')).first().id, amount = 1, unit = "unit")
    db.session.add(letture_ing)
    db.session.add(avocado_ing)
    db.session.commit()

    response = test_client.get('/index', follow_redirects = True)
    
    assert response.status_code == 200
    
    # check if you are in the right page
    assert b"Recommended based on your preferences and current ingredients" in response.data

    # there should be total two posts
    all_recipes = db.session.scalars(sqla.select(Recipe)).all()
    assert len(all_recipes) == 6

    # Avocado Toast and Salad matche preferences (vegan), so it should be in both sections
    assert response.data.count(b"Avocado Toast") == 4 # 2 * number of apperance since it has a front picture
    assert response.data.count(b"Tomato Salad") == 2
    assert response.data.count(b"Avocado Salad") == 2

    # Corn Soup is NOT vegan, so it should only appear once in the "All Recipes" section
    assert response.data.count(b"Corn Soup") == 2 # 2 * number of apperance since it has a front picture
    assert response.data.count(b"Trail Mix") == 1 # Trail Mix is vegan and easy, but it has peanuts so it should be not be recommended

    # Avocado Toast should appear before Salad since it has more matching tags with the user's preferred tags, so it should be ranked higher in the recommended section
    assert response.data.find(b"Avocado Toast") < response.data.find(b"Tomato Salad")

    # Avocado Salad should appear before Tomato Salad since it has more matching ingredients with the user's current ingredients, so it should be ranked higher in the recommended section
    assert response.data.find(b'Avocado Salad') < response.data.find(b"Tomato Salad")

def test_sortby_date_filterby_tags(test_client,init_database): # rewrite this test
    """
    GIVEN a Flask application configured for testing , after user logs-in, and sorts by date and filters by tags,
    THEN check that response is valid and the recommended recipes are updated in the database
    """
    # Login as CookingMama
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    add_recipe_posts(test_client, init_database)

    response = test_client.post('/index', data={
        'sortby': 'Date', 
        'tags': [db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first().id]
    }, follow_redirects = True)

    assert response.status_code == 200

    # check if you are in the right page
    assert b'All recipes (4)' in response.data
    assert b"Recommended based on your preferences and current ingredients" not in response.data

    # should only show the vegan recipes sorted by date (newest to oldest)
    assert b"Avocado Toast" in response.data
    assert b"Avocado Salad" in response.data
    assert b"Tomato Salad" in response.data
    assert b"Trail Mix" in response.data
    assert b"Corn Soup" not in response.data

    assert response.data.find(b'Trail Mix') < response.data.find(b"Avocado Salad") < response.data.find(b"Tomato Salad") < response.data.find(b"Avocado Toast")

def test_sortby_saves_filterby_min_saves(test_client,init_database): # rewrite this test
    """
    GIVEN a Flask application configured for testing , after user logs-in, and sorts by # of saves and filters by minimum save count,
    THEN check that response is valid and the recommended recipes are updated in the database
    """
    # Login as CookingMama
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    add_recipe_posts(test_client, init_database)

    response = test_client.post('/index', data={
        'sortby': '# of saves', 
        'saves': 2
    }, follow_redirects = True)

    assert response.status_code == 200

    # check if you are in the right page
    assert b'All recipes (4)' in response.data
    assert b"Recommended based on your preferences and current ingredients" not in response.data

    # should only show the recipes that has at least 2 saves, sorted by number of saves (highest to lowest)
    assert b"Avocado Toast" in response.data
    assert b"Avocado Salad" in response.data
    assert b"Tomato Salad" in response.data
    assert b"Trail Mix" not in response.data
    assert b"Corn Soup" in response.data

    assert response.data.find(b'Avocado Toast') < response.data.find(b"Corn Soup") < response.data.find(b"Tomato Salad") < response.data.find(b"Avocado Salad")


# ------------------------------------
# RECIPE ROUTES TESTS
def test_recipe_draft(test_client,init_database): # rewrite this test
    # """
    # GIVEN a Flask application configured for testing , after user logs in,
    # WHEN the '/post' page is requested (GET)  AND PostForm' form is submitted (POST)
    # THEN check that response is valid and the class is successfully created in the database
    # """
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    # check that recipe create leads to select recipe draft
    response = test_client.get('/recipe/create')
    assert response.status_code == 200
    assert b"Select Recipe Draft" in response.data

    # create a new recipe draft
    response = test_client.post('/recipe/create', data={"select_button":"new"}, follow_redirects = True)
    assert response.status_code == 200
    # check successful redirect
    assert b"Create New Recipe" in response.data
    # check the draft is in the db
    newDraft = db.session.scalars(sqla.select(Recipe).where(Recipe.is_draft == True)).first()
    assert newDraft is not None
    
    # check saving recipe draft
    response = test_client.post('/recipe/'+str(newDraft.id)+'/edit', data={
        "title":"Testing Drafts",
        "pictFile": (io.BytesIO(b""), ""),
        "description":"",
        "servingSize":0,
        "estimatedHrs":0,
        "estimatedMins":0,
        "tags":[],
        "ingredients":[],
        "steps":[],
        "action_button":"save",
    }, content_type="multipart/form-data", follow_redirects = True)

    assert response.status_code == 200
    # check successful redirect
    assert b"Welcome!" in response.data
    # check the draft is updated in the db
    updatedDraft = db.session.scalars(sqla.select(Recipe).where(Recipe.is_draft == True)).first()
    assert updatedDraft is not None
    assert updatedDraft.title == "Testing Drafts"

    # check that the draft appears in the options
    response = test_client.get('/recipe/create')
    assert response.status_code == 200
    assert b"Select Recipe Draft" in response.data
    assert b"Testing Drafts" in response.data

    # check editing the created draft
    response = test_client.post('/recipe/create', data={"select_button":str(updatedDraft.id)}, follow_redirects = True)
    assert response.status_code == 200
    # check successful redirect
    assert b"Create New Recipe" in response.data
    # check title is prepopulated
    assert b"Testing Drafts" in response.data

    # check deleting the created draft
    response = test_client.post('/recipe/create', data={"remove_button":str(updatedDraft.id)}, follow_redirects = True)
    assert response.status_code == 200
    # check successful redirect
    assert b"Select Recipe Draft" in response.data
    # check the draft has been deleted
    deletedDraft = db.session.get(Recipe, updatedDraft.id)
    assert deletedDraft is None

    # finally logout
    do_logout(test_client, path = '/user/logout') 
    pass

def test_view_recipe(test_client,init_database):
    # """
    # GIVEN a Flask application configured for testing , after user logs in,
    # WHEN the '/post' page is requested (GET)  AND PostForm' form is submitted (POST)
    # THEN check that response is valid and the class is successfully created in the database
    # """
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    #test the "post" form 
    response = test_client.get('/recipe/1/view')

    #checking the page content
    assert response.status_code == 200
    assert b"Avocado Sandwich" in response.data
    assert b"1.0 unit of Avocado" in response.data 
    assert b"2.0 unit of Bread" in response.data 

    # finally logout
    do_logout(test_client, path = '/user/logout') 
    pass

def test_delete_recipe(test_client, init_database):
    # """
    # GIVEN a Flask application configured for testing , after user logs in,
    # WHEN the '/post' page is requested (GET)  AND PostForm' form is submitted (POST)
    # THEN check that response is valid and the class is successfully created in the database
    # """
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    # test deleting the recipe
    response = test_client.post('/recipe/1/delete', follow_redirects=True)
    # checking the page content
    assert response.status_code == 200
    # check redirect
    assert b"Welcome!" in response.data
    # check flash message
    assert b"Recipe has been successfully deleted" in response.data
    
    # # test error deleting the recipe
    response = test_client.post('/recipe/1/delete', follow_redirects=True)
    # checking the page content
    # check redirect
    assert b"Welcome!" in response.data
    # check flash message
    assert b"Error: recipe failed to delete" in response.data

    # finally logout
    do_logout(test_client, path = '/user/logout') 
    pass

def test_view_invalid_recipe(test_client, init_database):
    # """
    # GIVEN a Flask application configured for testing , after user logs in,
    # WHEN the '/post' page is requested (GET)  AND PostForm' form is submitted (POST)
    # THEN check that response is valid and the class is successfully created in the database
    # """
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    # test deleting the recipe
    response = test_client.get('/recipe/1000/view', follow_redirects=True)
    # assert response.status_code == 200
    # assert b"Welcome to Smile Portal!" in response.data
    # assert b"Second post" in response.data 
    # assert b"Here is another post." in response.data 

    # #checking whether the database is updated correctly with the post request 
    # thepost = db.session.scalars(sqla.select(Post).where(Post.title =='Second post')).first()
    # tags_of_post = thepost.get_tags()
    # assert (len(tags_of_post))== 2 #should have 2 tags
    # assert all_tags[1] in tags_of_post  #second tag should be one of the tags of the post. 

    # #there should be total two posts
    # all_posts = db.session.scalars(sqla.select(Post)).all()
    # assert len(all_posts) == 2

    # #finally logout
    # do_logout(test_client, path = '/user/logout') 
    pass

# ------------------------------------
# COOKBOOK ROUTES TESTS
def test_create_cookbook(test_client,init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == 'CookingMama')).first()
    assert user is not None
    user.is_certified = True
    db.session.commit()
    db.session.refresh(user)
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    #add recipe to the user profile
    recipe = Recipe(title='Test Recipe', description='This is a test recipe.', user_id=user.id)
    db.session.add(recipe)
    recipe.is_draft = False
    db.session.commit()
    recipe2 = Recipe(title='Test Recipe 2', description='This is a test recipe.', user_id=user.id)
    db.session.add(recipe2)
    recipe2.is_draft = False
    db.session.commit()
    all_recipes = db.session.scalars(sqla.select(Recipe).where(Recipe.user_id == user.id)).all()
    recipes = list(map(lambda r: r.id, all_recipes[:2]))
    # test the "create cookbook" form
    response = test_client.get('/cookbook/create')
    assert response.status_code == 200
    assert b"Create Cookbook" in response.data
    response = test_client.post('/cookbook/create', 
                          data=dict(title='Test Cookbook', pictFile=None, description='This is a test cookbook.', recipes=recipes, submit='Post'),
                          follow_redirects = True)
    assert response.status_code == 200
    cookbook = db.session.scalars(sqla.select(Cookbook)).first()
    assert cookbook is not None
    assert recipe in cookbook.get_recipes()
    # logout
    do_logout(test_client, path = '/user/logout')

def test_create_cookbook_no_recipes(test_client,init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == 'CookingMama')).first()
    assert user is not None
    user.is_certified = True
    db.session.commit()
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    # test the "create cookbook" form with no recipes selected
    response = test_client.post('/cookbook/create', 
                          data=dict(title='Test Cookbook', pictFile=None, description='This is a test cookbook.', recipes=[], submit='Post'),
                          follow_redirects = True)
    assert response.status_code == 200
    # logout
    do_logout(test_client, path = '/user/logout')

def test_create_cookbook_not_certified(test_client,init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == 'CookingMama')).first()
    assert user is not None
    user.is_certified = False
    db.session.commit()
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    # test the "create cookbook" form with no recipes selected
    response = test_client.get('/cookbook/create')
    assert response.status_code == 302
    # logout
    do_logout(test_client, path = '/user/logout')

def test_view_cookbook(test_client,init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == 'CookingMama')).first()
    assert user is not None
    user.is_certified = True
    db.session.commit()
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    #add cookbook to the database
    cookbook = Cookbook(title='Test Cookbook', description='This is a test cookbook.', user_id=user.id)
    db.session.add(cookbook)
    db.session.commit()
    recipe = Recipe(title='Test Recipe', description='This is a test recipe.', user_id=user.id)
    db.session.add(recipe)
    recipe.is_draft = False
    db.session.commit()
    cookbook.included_recipes.add(recipe)
    db.session.commit()
    # test the "view cookbook" page
    response = test_client.get('/cookbook/{c}/view'.format(c=cookbook.id))
    assert response.status_code == 200
    assert b"Test Cookbook" in response.data
    assert b"Test Recipe" in response.data
    # logout
    do_logout(test_client, path = '/user/logout')

def test_view_cookbook_invalid_id(test_client,init_database):
    response = test_client.get('/cookbook/999/view')
    assert response.status_code == 302

def test_edit_cookbook(test_client,init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == 'CookingMama')).first()
    assert user is not None
    user.is_certified = True
    db.session.commit()
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    #add cookbook to the database
    cookbook = Cookbook(title='Test Cookbook', description='This is a test cookbook.', user_id=user.id)
    db.session.add(cookbook)
    db.session.commit()
    recipe = Recipe(title='Test Recipe', description='This is a test recipe.', user_id=user.id)
    db.session.add(recipe)
    recipe.is_draft = False
    db.session.commit()
    cookbook.included_recipes.add(recipe)
    db.session.commit()
    recipe2 = Recipe(title='Test Recipe 2', description='This is another test recipe.', user_id=user.id)
    db.session.add(recipe2)
    recipe2.is_draft = False
    db.session.commit()
    # test the "edit cookbook" page
    response = test_client.post('/cookbook/{c}/edit'.format(c=cookbook.id),
                                data=dict(title='Updated Cookbook', pictFile=None, description='This is an updated test cookbook.', recipes=[recipe2.id], submit='Post'),
                          follow_redirects = True)
    assert response.status_code == 200
    cookbook = db.session.get(Cookbook, cookbook.id)
    assert cookbook.title == 'Updated Cookbook'
    assert cookbook.description == 'This is an updated test cookbook.'
    assert recipe2 in cookbook.get_recipes()
    assert recipe not in cookbook.get_recipes()
    # logout
    do_logout(test_client, path = '/user/logout')
def test_edit_cookbook_invalid_id(test_client,init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == 'CookingMama')).first()
    assert user is not None
    user.is_certified = True
    db.session.commit()
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    response = test_client.get('/cookbook/999/edit')
    assert response.status_code == 302
    # logout
    do_logout(test_client, path = '/user/logout')

def test_get_edit_cookbook(test_client,init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == 'CookingMama')).first()
    assert user is not None
    user.is_certified = True
    db.session.commit()
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    #add cookbook to the database
    cookbook = Cookbook(title='Test Cookbook', description='This is a test cookbook.', user_id=user.id)
    db.session.add(cookbook)
    db.session.commit()
    recipe = Recipe(title='Test Recipe', description='This is a test recipe.', user_id=user.id)
    db.session.add(recipe)
    recipe.is_draft = False
    db.session.commit()
    cookbook.included_recipes.add(recipe)
    db.session.commit()
    # test the "edit cookbook" page
    response = test_client.get('/cookbook/{c}/edit'.format(c=cookbook.id))
    assert response.status_code == 200
    assert b"Create Cookbook" in response.data
    assert b"Test Cookbook" in response.data
    assert b"This is a test cookbook." in response.data
    assert b"Test Recipe" in response.data
    # logout
    do_logout(test_client, path = '/user/logout')

def test_delete_cookbook(test_client,init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == 'CookingMama')).first()
    assert user is not None
    user.is_certified = True
    db.session.commit()
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    #add cookbook to the database
    cookbook = Cookbook(title='Test Cookbook', description='This is a test cookbook.', user_id=user.id)
    db.session.add(cookbook)
    db.session.commit()
    recipe = Recipe(title='Test Recipe', description='This is a test recipe.', user_id=user.id)
    db.session.add(recipe)
    recipe.is_draft = False
    db.session.commit()
    cookbook.included_recipes.add(recipe)
    db.session.commit()
    # test the "delete cookbook" page
    response = test_client.post('/cookbook/{c}/delete'.format(c=cookbook.id), follow_redirects=True)
    assert response.status_code == 200
    cookbook = db.session.get(Cookbook, cookbook.id)
    assert cookbook is None
    # logout
    do_logout(test_client, path = '/user/logout')

def test_delete_cookbook_no_cookbook(test_client,init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == 'CookingMama')).first()
    assert user is not None
    user.is_certified = True
    db.session.commit()
    # login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    response = test_client.post('/cookbook/999/delete', follow_redirects=True)
    assert response.status_code == 200
    # logout
    do_logout(test_client, path = '/user/logout')

# ------------------------------------
# USER ROUTES TESTS
def test_display_profile_not_authenticated(test_client, init_database):
    response = test_client.get('/user/profile', follow_redirects=False)
    assert response.status_code == 302
    assert '/user/login' in response.headers['Location']

def test_display_profile_regular(test_client, init_database):
    # Log into regular user account
    user = db.session.scalars(sqla.select(User).where(User.username == "notcertified")).first()
    
    do_login(test_client, path = '/user/login', username = 'notcertified', passwd = '123')
    recipe1 = new_recipe("Recipe1", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    recipe2 = new_recipe("Recipe2", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    db.session.add(recipe1)
    db.session.add(recipe2)
    db.session.commit()

    # Get user profile
    response = test_client.get('user/profile')
    assert response.status_code == 200

    # Expected title
    expected_title = "{} {}'s Profile".format(user.first_name, user.last_name)
    assert expected_title.encode() in response.data

    # Assert all user recipes displayed
    for recipe in user.get_user_recipes():
        assert recipe.title.encode() in response.data
    
    # Expected default state of the view
    assert b"My Posts" in response.data

    # Assert no cookbook field in profile (not certified)
    assert b"Number of Cookbooks Posted" not in response.data

    do_logout(test_client, path = 'user/logout')

def test_display_profile_certified(test_client, init_database):    
    # Log into regular user account
    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()
    # Make user certified
    user.is_certified = True
    db.session.commit()
    assert user.is_certified == True

    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    # Add user recipes
    recipe1 = new_recipe("Recipe1", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    recipe2 = new_recipe("Recipe2", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    db.session.add(recipe1)
    db.session.add(recipe2)
    db.session.commit()

    # Add cookbook
    cookbook = Cookbook(title='Test Cookbook', description='This is a test cookbook.', user_id=user.id)
    db.session.add(cookbook)
    db.session.commit()

    # Add recipes to cookbook
    cookbook.included_recipes.add(recipe1)
    cookbook.included_recipes.add(recipe2)
    db.session.commit()

    # Get user profile
    response = test_client.get('user/profile')
    assert response.status_code == 200

    # Expected title
    expected_title = "{} {}'s Profile".format(user.first_name, user.last_name)
    assert expected_title.encode() in response.data

    # Assert all user recipes displayed
    for recipe in user.get_user_recipes():
        assert recipe.title.encode() in response.data
    
    # Expected default state of the view
    assert b"My Posts" in response.data

    # There should be a cookbook field displayed on the profile
    assert b"Number of Cookbooks Posted" in response.data

    # Test for Cookbooks
    response = test_client.get('user/profile?view=cookbook')
    assert response.status_code == 200

    # Expected title
    expected_title = "{} {}'s Profile".format(user.first_name, user.last_name)
    assert expected_title.encode() in response.data
    
    # Expected default state of the view
    assert b"My Cookbooks" in response.data

    # Check that the cookbooks are displayed
    for cookbook in user.get_user_cookbooks():
        assert cookbook.title.encode() in response.data

    do_logout(test_client, path = 'user/logout')

def test_view_other_profile(test_client, init_database):
    # Get tags for dietary restrictions and preferred tags
    vegan_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first()
    easy_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'easy')).first()

    # Add another user    
    user = new_user(first_name='Ash', last_name='Lynx', username='theBoss', email='ashlynx@wpi.edu', password='123',
                    dietary_tags=[vegan_tag], preferred_tags=[easy_tag])
    # Insert user data
    db.session.add(user)
    db.session.commit()

    # Add user recipes
    recipe1 = new_recipe("Recipe1", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    recipe2 = new_recipe("Recipe2", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    db.session.add(recipe1)
    db.session.add(recipe2)
    db.session.commit()

    # First, test that we are redirected to the login page if we are not logged in.
    response = test_client.get(f"/user/{user.id}/viewprofile", follow_redirects=False)
    assert response.status_code == 302
    assert '/user/login' in response.headers['Location']
    
    # Login
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    # Get user profile
    response = test_client.get(f"/user/{user.id}/viewprofile", follow_redirects=False)
    assert response.status_code == 200

    # Expected title
    expected_title = "{} {}'s Profile".format(user.first_name, user.last_name)
    assert expected_title.encode() in response.data

    # Assert all user recipes displayed
    for recipe in user.get_user_recipes():
        assert recipe.title.encode() in response.data
    
    # Expected default state of the view
    view_title=f"{user.first_name}'s Posts"
    assert view_title.encode() in response.data

    # Logout
    do_logout(test_client, path = 'user/logout')

def view_other_profile_invalid_id(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    response = test_client.get(f"/user/999/viewprofile", follow_redirects=False)
    assert response.status_code == 302
    do_logout(test_client, path = 'user/logout')
    
def test_edit_profile(test_client, init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()
    vegan_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first()
    vegetarian_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegetarian')).first()
    easy_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'easy')).first()
    breakfast_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'breakfast')).first()
    # Login as CookingMama
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    response = test_client.post('/user/profile/edit', 
                          data=dict(username = "NewCM", 
                                    first_name="New", 
                                    last_name="Last", 
                                    email="new@email.com", 
                                    allergies=None, 
                                    dietary_restrictions = [str(vegetarian_tag.id), str(vegan_tag.id)],
                                    tags = [str(easy_tag.id)]), follow_redirects = False)
    assert response.status_code == 302
    assert '/user/profile' in response.headers['Location']
    editedUser = db.session.scalars(sqla.select(User).where(User.id == user.id)).first()
    assert editedUser.username == "NewCM"
    assert editedUser.first_name == "New"
    assert editedUser.last_name == "Last"
    assert editedUser.email == "new@email.com"
    allergies = editedUser.get_user_allergies()
    assert allergies == []
    dietary_tags = editedUser.get_dietary_tags()
    assert vegan_tag in dietary_tags
    assert vegetarian_tag in dietary_tags
    pref_tags = editedUser.get_preferred_tags()
    assert easy_tag in pref_tags
    assert breakfast_tag not in pref_tags
    # Logout
    do_logout(test_client, path = 'user/logout')

def test_edit_profile_certified(test_client, init_database):
    c0 = Certification(
    name = "Certified Fundamental Cook")
    c1 = Certification(
        name = "Certified Sous Cook")
    db.session.add(c0)
    db.session.add(c1)
    db.session.commit()
    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()
    user.is_certified = True
    db.session.commit()
    uc0 = UserCertification(user_id=user.id, certification_id=c0.id, dateRecieved = datetime.now())
    db.session.add(uc0)
    vegan_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first()
    vegetarian_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegetarian')).first()
    easy_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'easy')).first()
    breakfast_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'breakfast')).first()
    # Login as CookingMama
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    # Has to be flattened for cert in eform.certifications.data to be true
    response = test_client.post('/user/profile/edit',
                                data={"username": "NewCM",
                                      "first_name": "New",
                                      "last_name": "Last",
                                      "email": "new@email.com",
                                      "allergies": [],
                                      "dietary_restrictions": [
                                          str(vegetarian_tag.id),
                                          str(vegan_tag.id)],
                                      "tags": [str(easy_tag.id)],
                                      "certifications-0-certifications": str(c1.id),
                                      "certifications-0-dateRecieved": "2026-03-03",
                                      "submit": "Update"}, follow_redirects=False)
    assert response.status_code == 302
    assert '/user/profile' in response.headers['Location']
    editedUser = db.session.scalars(sqla.select(User).where(User.id == user.id)).first()
    assert editedUser.username == "NewCM"
    assert editedUser.first_name == "New"
    assert editedUser.last_name == "Last"
    assert editedUser.email == "new@email.com"
    allergies = editedUser.get_user_allergies()
    assert allergies == []
    dietary_tags = editedUser.get_dietary_tags()
    assert vegan_tag in dietary_tags
    assert vegetarian_tag in dietary_tags
    pref_tags = editedUser.get_preferred_tags()
    assert easy_tag in pref_tags
    assert breakfast_tag not in pref_tags
    user_certs = editedUser.get_certifications()
    assert c1.name == user_certs[0].name
    # Logout
    do_logout(test_client, path = 'user/logout')

def test_edit_profile_username_exists(test_client, init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()
    vegan_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first()
    easy_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'easy')).first()
    # Add another user    
    user2 = new_user(first_name='Ash', last_name='Lynx', username='theBoss', email='ashlynx@wpi.edu', password='123',
                    dietary_tags=[vegan_tag], preferred_tags=[easy_tag])
    # Insert user data
    db.session.add(user2)
    db.session.commit()
    # Login as CookingMama
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    
    response = test_client.post('/user/profile/edit', 
                        data=dict(username = "theBoss", 
                                    first_name="New", 
                                    last_name="Last", 
                                    email="new@email.com"), follow_redirects = True)
    assert response.status_code == 200
    assert b"This username is already registered!" in response.data
    editedUser = db.session.scalars(sqla.select(User).where(User.id == user.id)).first()
    assert editedUser.username == "CookingMama"
    assert editedUser.first_name == "Cooking"
    # Logout
    do_logout(test_client, path = 'user/logout')

def test_edit_profile_email_exists(test_client, init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()
    vegan_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first()
    easy_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'easy')).first()
    # Add another user    
    user2 = new_user(first_name='Ash', last_name='Lynx', username='theBoss', email='ashlynx@wpi.edu', password='123',
                    dietary_tags=[vegan_tag], preferred_tags=[easy_tag])
    # Insert user data
    db.session.add(user2)
    db.session.commit()
    # Login as CookingMama
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    response = test_client.post('/user/profile/edit', 
                        data=dict(username = "NewUser", 
                                    first_name="New", 
                                    last_name="Last", 
                                    email="ashlynx@wpi.edu"), follow_redirects = True)
    assert response.status_code == 200
    assert b"This email is already registered! Please provide a different email address." in response.data
    editedUser = db.session.scalars(sqla.select(User).where(User.id == user.id)).first()
    assert editedUser.username == "CookingMama"
    assert editedUser.first_name == "Cooking"
    assert editedUser.email == "cookingmama@wpi.edu"
    # Logout
    do_logout(test_client, path = 'user/logout')

def test_become_certified_regular(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    c0 = Certification(
    name = "Certified Fundamental Cook")
    db.session.add(c0)
    db.session.commit()
    response = test_client.get('/user/profile/certify')
    assert response.status_code == 200
    # Verify session data and get the ot_code
    with test_client.session_transaction() as sess:
        ot_code = sess.get('ot_code')
    response2 = test_client.post('/user/profile/certify', 
                                 data={"certifications-0-certifications": str(c0.id),
                                      "certifications-0-dateRecieved": "2026-03-03",
                                      "in_code" : ot_code,
                                      "submit": "Update"},
                                follow_redirects=False)
    assert response2.status_code == 302
    assert '/user/profile' in response2.headers['Location']
    
    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()
    assert user.is_certified == True
    # Logout
    do_logout(test_client, path = 'user/logout')

def test_become_certified_regular_wrong_code(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    c0 = Certification(name = "Certified Fundamental Cook")
    db.session.add(c0)
    db.session.commit()
    response = test_client.get('/user/profile/certify')
    assert response.status_code == 200
    # Verify session data and get the ot_code
    with test_client.session_transaction() as sess:
        ot_code = sess.get('ot_code')
    code = 0000000
    response2 = test_client.post('/user/profile/certify', 
                                 data={"certifications-0-certifications": str(c0.id),
                                      "certifications-0-dateRecieved": "2026-03-03",
                                      "in_code" : code,
                                      "submit": "Update"},
                                follow_redirects=False)
    assert response2.status_code == 200
    
    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()
    assert user.is_certified == False
    # Logout
    do_logout(test_client, path = 'user/logout')
    
def test_become_certified_already_certified(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()
    user.is_certified = True
    db.session.commit()
    response = test_client.get('/user/profile/certify', follow_redirects=False)
    assert response.status_code == 302
    assert '/index' in response.headers['Location']
    
     # Logout
    do_logout(test_client, path = 'user/logout')

def test_save_recipe(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()

    # Add recipes
    recipe1 = new_recipe("Recipe1", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    recipe2 = new_recipe("Recipe2", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    db.session.add(recipe1)
    db.session.add(recipe2)
    db.session.commit()

    response = test_client.post(f"/user/{recipe1.id}/saverecipe", follow_redirects = True)
    assert response.status_code == 200
    assert recipe1.save_count == 1
    assert recipe2.save_count == 0

    response2 = test_client.get("user/profile?view=saved")
    assert response2.status_code == 200
    assert recipe1.title.encode() in response2.data

    assert recipe1 in user.get_saved()

    do_logout(test_client, path = 'user/logout')


def test_save_recipe_already_saved(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()

    # Add recipes
    recipe1 = new_recipe("Recipe1", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    db.session.add(recipe1)
    db.session.commit()

    user.saved_recipes.add(recipe1)
    db.session.commit()
    recipe1.save_count += 1
    assert recipe1 in user.get_saved()

    response = test_client.post(f"/user/{recipe1.id}/saverecipe", follow_redirects = True)
    assert response.status_code == 200
    assert recipe1.save_count == 1
    assert b"You have already saved this recipe!" in response.data
    assert recipe1 in user.get_saved()

    do_logout(test_client, path = 'user/logout')

def test_remove_saved_recipe(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()

    # Add recipes
    recipe1 = new_recipe("Recipe1", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    db.session.add(recipe1)
    db.session.commit()

    user.saved_recipes.add(recipe1)
    db.session.commit()
    recipe1.save_count += 1
    assert recipe1 in user.get_saved()

    response = test_client.post(f"/user/{recipe1.id}/removerecipe", follow_redirects = True)
    assert response.status_code == 200
    assert recipe1.save_count == 0
    assert user.get_saved() == []

    do_logout(test_client, path = 'user/logout')

def test_save_with_ingredients(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalars(sqla.select(User).where(User.username == "CookingMama")).first()

    # Add recipes
    recipe1 = new_recipe("Recipe1", "description", 2, 1, 0, datetime.now(), False, user.id, save_count=0, pictFile=None)
    db.session.add(recipe1)
    db.session.commit()

    # Add ingredients to the recipe
    onion = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Onion")).first()
    cream = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Cream")).first()
    corn = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Corn")).first()
    
    ri00 = RecipeIngredientUse(recipe_id = recipe1.id, ingredient_id = onion.id, amount = 0.5, unit = "unit")
    db.session.add(ri00)
    ri01 = RecipeIngredientUse(recipe_id = recipe1.id, ingredient_id = cream.id, amount = 1, unit = "unit")
    db.session.add(ri01)
    ri02 = RecipeIngredientUse(recipe_id = recipe1.id, ingredient_id = corn.id, amount = 4, unit = "tbsp")
    db.session.add(ri02)
    db.session.commit()

    ingredient_list = recipe1.get_ingredient_use_cases()
    
    response = test_client.post(f"/user/{recipe1.id}/saverecipe", 
                                data={"ingredient_ids" : [ingred.ingredient_id for ingred in ingredient_list]},
                                follow_redirects = True)
    assert response.status_code == 200
    assert recipe1.save_count == 1
    assert recipe1 in user.get_saved()
    for ingred in ingredient_list:
        assert (ingred.ingredient_id, 
                ingred.amount, 
                ingred.unit) in [(i.ingredient_id, i.amount, i.unit) 
                                 for i in user.get_grocery_list()]

    do_logout(test_client, path = 'user/logout')

def test_add_and_view_current_ingredients(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalar(sqla.select(User).where(User.username == "CookingMama"))
    onion = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Onion")).first()

    response = test_client.post('/user/ingredients',
                                data={"curr-ingredientName": onion.name,
                                      "curr-quantity": 3,
                                      "curr-submit": True},
                                follow_redirects=False)
    
    current_list = user.get_curr_ingredients()
    assert (onion.id, 3, "unit") in [(ing.ingredient_id, ing.amount, ing.unit) for ing in current_list]

    response = test_client.get('/user/ingredients')

    assert response.status_code == 200
    assert onion.name.encode() in response.data
    assert b"3" in response.data
    assert b"unit" in response.data
    do_logout(test_client, path = 'user/logout')

def test_view_grocery_ingredients(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalar(sqla.select(User).where(User.username == "CookingMama"))
    onion = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Onion")).first()

    response = test_client.post('/user/ingredients',
                                data={"groc-ingredientName": onion.name,
                                      "groc-quantity": 0.5,
                                      "groc-unit" : "lb",
                                      "groc-submit": True},
                                follow_redirects=False)
    
    grocery_list = user.get_grocery_list()
    assert (onion.id, 0.5, "lb") in [(ing.ingredient_id, ing.amount, ing.unit) for ing in grocery_list]

    response = test_client.get('/user/ingredients')

    assert response.status_code == 200
    assert onion.name.encode() in response.data
    assert b"0.5" in response.data
    assert b"lb" in response.data
    do_logout(test_client, path = 'user/logout')

def test_move_grocery(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalar(sqla.select(User).where(User.username == "CookingMama"))
    onion = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Onion")).first()

    user_groc = UserGroceryListUse(user_id = user.id, ingredient_id = onion.id, amount = 0.5, unit = "unit")
    db.session.add(user_groc)
    db.session.commit()

    grocery_list = user.get_grocery_list()
    assert user_groc in grocery_list

    response = test_client.post('/user/move_or_delete_grocery',
                                data={"action": "purchased",
                                      "grocery_ids": [str(onion.id)]},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Selected ingredients moved to current ingredients." in response.data

    db.session.refresh(user)
    grocery_list = user.get_grocery_list()
    assert grocery_list == []

    # Ingredient should now exist in current ingredients
    current_list = user.get_curr_ingredients()
    assert (onion.id, 0.5, "unit") in [(ing.ingredient_id, ing.amount, ing.unit) for ing in current_list]
    
    do_logout(test_client, path = 'user/logout')

def test_delete_grocery(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalar(sqla.select(User).where(User.username == "CookingMama"))
    onion = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Onion")).first()

    user_groc = UserGroceryListUse(user_id = user.id, ingredient_id = onion.id, amount = 0.5, unit = "unit")
    db.session.add(user_groc)
    db.session.commit()

    grocery_list = user.get_grocery_list()
    assert user_groc in grocery_list

    response = test_client.post('/user/move_or_delete_grocery',
                                data={"action": "delete",
                                      "grocery_ids": [str(onion.id)]},
                                follow_redirects=True)

    assert response.status_code == 200
    assert b"Selected grocery items deleted." in response.data


    db.session.refresh(user)
    grocery_list = user.get_grocery_list()
    assert grocery_list == []
    current_list = user.get_curr_ingredients()
    assert current_list == []
    
    do_logout(test_client, path = 'user/logout')

def test_delete_ingredient(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalar(sqla.select(User).where(User.username == "CookingMama"))
    onion = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Onion")).first()

    user_ing = UserIngredientListUse(user_id = user.id, ingredient_id = onion.id, amount = 0.5, unit = "unit")
    db.session.add(user_ing)
    db.session.commit()

    curr_list = user.get_curr_ingredients()
    assert user_ing in curr_list

    response = test_client.post('/user/delete_ingredient',
                                data={"ingredient_ids": [onion.id]},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Selected ingredients deleted." in response.data

    db.session.refresh(user)
    current_list = user.get_curr_ingredients()
    assert current_list == []
    
    do_logout(test_client, path = 'user/logout')

def test_add_existing_ingredient_cost(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    onion = Ingredient(name = "onion")
    db.session.add(onion)
    db.session.commit()

    user = db.session.scalar(sqla.select(User).where(User.username == "CookingMama"))
    onion = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "onion")).first()

    response = test_client.post('/user/ingredientinfo',
                                data={"ingredientName": onion.name,
                                      "price": 0.5,
                                      "amount": 1,
                                      "unit": "unit",
                                      "submit": True},
                                      follow_redirects=True)
    assert response.status_code == 200

    cost_entry = db.session.scalars(sqla.select(IngredientCostEntry)
                                   .where(IngredientCostEntry.user_id == user.id)
                                   ).first()
    assert cost_entry.ingredient_id == onion.id

    assert cost_entry is not None
    assert cost_entry.cost == 0.5
    assert cost_entry.amount == 1
    assert cost_entry.unit == "unit"
    assert onion.name.encode() in response.data

    do_logout(test_client, path = 'user/logout')

def test_add_non_existing_ingredient_cost(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalar(sqla.select(User).where(User.username == "CookingMama"))

    response = test_client.post('/user/ingredientinfo',
                                data={"ingredientName": "Miso Paste",
                                      "price": 5,
                                      "amount": 1,
                                      "unit": "oz",
                                      "submit": True},
                                      follow_redirects=True)
    assert response.status_code == 200

    ingredient = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Miso Paste".lower())).first()

    cost_entry = db.session.scalars(sqla.select(IngredientCostEntry)
                                   .where(IngredientCostEntry.user_id == user.id)
                                   .where(IngredientCostEntry.ingredient_id == ingredient.id)).first()

    assert cost_entry is not None
    assert cost_entry.cost == 5
    assert cost_entry.amount == 1
    assert cost_entry.unit == "oz"
    assert ingredient.name.encode() in response.data

    do_logout(test_client, path = 'user/logout')

def test_ingredient_info_replace_existing(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    onion = Ingredient(name = "onion")
    db.session.add(onion)
    db.session.commit()
    user = db.session.scalar(sqla.select(User).where(User.username == "CookingMama"))
    onion = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "onion")).first()

    existing_cost_entry = IngredientCostEntry(user_id = user.id, ingredient_id = onion.id, cost = 5, amount = 2, unit = "unit")
    db.session.add(existing_cost_entry)
    db.session.commit()

    response = test_client.post('/user/ingredientinfo',
                                data={"ingredientName": onion.name,
                                      "price": 0.5,
                                      "amount": 1,
                                      "unit": "unit",
                                      "submit": True},
                                      follow_redirects=True)
    assert response.status_code == 200

    cost_entry = db.session.scalars(sqla.select(IngredientCostEntry)
                                   .where(IngredientCostEntry.user_id == user.id)
                                   .where(IngredientCostEntry.ingredient_id == onion.id)).first()
    assert cost_entry.ingredient_id == onion.id

    assert cost_entry is not None
    assert cost_entry.cost == 0.5
    assert cost_entry.amount == 1
    assert cost_entry.unit == "unit"
    assert onion.name.encode() in response.data

def test_invalid_price(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalar(sqla.select(User).where(User.username == "CookingMama"))

    response = test_client.post('/user/ingredientinfo',
                                data={"ingredientName": "Miso Paste",
                                      "price": 0,
                                      "amount": 1,
                                      "unit": "oz",
                                      "submit": True},
                                      follow_redirects=True)
    assert response.status_code == 200

    ingredient = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Miso Paste".lower())).first()

    cost_entry = db.session.scalars(sqla.select(IngredientCostEntry)
                                   .where(IngredientCostEntry.user_id == user.id)).first()

    assert ingredient is None
    assert cost_entry is None
    assert b"Ingredient price must be greater than 0" in response.data

    do_logout(test_client, path = 'user/logout')

def test_invalid_amount(test_client, init_database):
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')

    user = db.session.scalar(sqla.select(User).where(User.username == "CookingMama"))

    response = test_client.post('/user/ingredientinfo',
                                data={"ingredientName": "Miso Paste",
                                      "price": 5,
                                      "amount": 0,
                                      "unit": "oz",
                                      "submit": True},
                                      follow_redirects=True)
    assert response.status_code == 200

    ingredient = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == "Miso Paste".lower())).first()

    cost_entry = db.session.scalars(sqla.select(IngredientCostEntry)
                                   .where(IngredientCostEntry.user_id == user.id)).first()

    assert ingredient is None
    assert cost_entry is None
    assert b"Ingredient amount must be greater than 0" in response.data
    
    # finally logout
    do_logout(test_client, path = '/user/logout') 
    pass

def test_recipe_step_operations(test_client, init_database):
    do_login(test_client, path='/user/login', username='CookingMama', passwd='123')

    # Create draft
    test_client.post('/recipe/create', data={"select_button": "new"}, follow_redirects=True)
    draft = db.session.scalars(sqla.select(Recipe).where(Recipe.is_draft == True)).first()
    # check that the draft was created
    assert draft is not None

    # edit the draft data
    response = test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "title": "Testing Steps",
            "description": "",
            "servingSize": 1,
            "estimatedHrs": 0,
            "estimatedMins": 0,
            "tags": [],
            "ingredients": [],
            "steps-0-stepDescription": "First step",
            "steps-1-stepDescription": "Second step",
            "pictFile": (io.BytesIO(b""), ""),
            "action_button": "add", # adding steps
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )
    assert response.status_code == 200
    # check that the steps appear
    assert b"First step" in response.data
    assert b"Second step" in response.data

    # check that the steps are in the db
    steps = db.session.scalars(sqla.select(RecipeStep).where(RecipeStep.recipe_id == draft.id)).all()
    assert len(steps) == 2

    # move step down
    firstStep = steps[0]
    test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "step_down_button": str(firstStep.id),
            "pictFile": (io.BytesIO(b""), "")
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )
    newFirstStep = db.session.scalars(sqla.select(RecipeStep).where(RecipeStep.recipe_id == draft.id).where(RecipeStep.stepNum == 1)).first()
    newSecondStep = db.session.scalars(sqla.select(RecipeStep).where(RecipeStep.recipe_id == draft.id).where(RecipeStep.stepNum == 2)).first()
    assert newFirstStep.description == "Second step"
    assert newSecondStep.description == "First step"

    # move step back up
    test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "step_up_button": str(firstStep.id),
            "pictFile": (io.BytesIO(b""), "")
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )
    newFirstStep = db.session.scalars(sqla.select(RecipeStep).where(RecipeStep.recipe_id == draft.id).where(RecipeStep.stepNum == 1)).first()
    newSecondStep = db.session.scalars(sqla.select(RecipeStep).where(RecipeStep.recipe_id == draft.id).where(RecipeStep.stepNum == 2)).first()
    assert newFirstStep.description == "First step"
    assert newSecondStep.description == "Second step"

    # check deleting a step
    test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "step_remove_button": str(newFirstStep.id),
            "pictFile": (io.BytesIO(b""), "")
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )

    deleted_step = db.session.get(RecipeStep, newFirstStep.id)
    assert deleted_step is None

    do_logout(test_client, path='/user/logout')

def test_recipe_ingredient_operations(test_client, init_database):
    do_login(test_client, path='/user/login', username='CookingMama', passwd='123')

    # get an ingredient
    ingredient = db.session.scalars(
        sqla.select(Ingredient)
    ).first()
    assert ingredient is not None

    # Create draft
    test_client.post(
        '/recipe/create',
        data={"select_button": "new"},
        follow_redirects=True
    )

    # check that the draft exists
    draft = db.session.scalars(sqla.select(Recipe).where(Recipe.is_draft == True)).first()
    assert draft is not None

    # add an ingredient
    response = test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "title": "Ingredient Test",
            "description": "",
            "servingSize": 1,
            "estimatedHrs": 0,
            "estimatedMins": 0,
            "tags": [],
            "ingredients-0-ingredientName": ingredient.name,
            "ingredients-0-quantity": 2,
            "ingredients-0-unit": "cup",
            "ingredients-0-ingredient_id": ingredient.id,
            "action_button": "add",
            "pictFile": (io.BytesIO(b""), "")
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )

    # check that there is now one ingredient use
    uses = db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == draft.id)).all()
    assert len(uses) == 1

    
    # check removing ingredient
    response = test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "title": "Ingredient Test",
            "description": "",
            "servingSize": 1,
            "estimatedHrs": 0,
            "estimatedMins": 0,
            "tags": [],
            "ingredients-0-ingredientName": ingredient.name,
            "ingredients-0-quantity": 2,
            "ingredients-0-unit": "cup",
            "ingredients-0-ingredient_id": ingredient.id,
            "pictFile": (io.BytesIO(b""), ""),
            "action_button": str(ingredient.id), # remove this ingredient
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )

    # check that the redirect was successful
    assert b"Create New Recipe" in response.data

    # check deletion successfull
    deleted_use = db.session.scalars(
        sqla.select(RecipeIngredientUse).where(
            RecipeIngredientUse.recipe_id == draft.id,
            RecipeIngredientUse.ingredient_id == ingredient.id
        )
    ).first()
    assert deleted_use is None

    do_logout(test_client, path='/user/logout')

def test_post_recipe(test_client, init_database):
    # login
    do_login(test_client, path='/user/login',
             username='CookingMama', passwd='123')

    # get ingredient
    ingredient = db.session.scalars(sqla.select(Ingredient)).first()
    # check that it exists
    assert ingredient is not None
    
    # create a draft
    test_client.post(
        '/recipe/create',
        data={"select_button": "new"},
        follow_redirects=True
    )
    # check that it is in db
    draft = db.session.scalars(sqla.select(Recipe).where(Recipe.is_draft == True)).first()
    assert draft is not None

    # post recipe
    response = test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "title": "Simple Mix",
            "description": "Simple recipe with 1 ingredient",
            "servingSize": 2,
            "estimatedHrs": "0",
            "estimatedMins": "15",
            "tags": [],
            "ingredients-0-ingredient_id": str(ingredient.id),
            "ingredients-0-ingredientName": ingredient.name,
            "ingredients-0-quantity": 1,
            "ingredients-0-unit": "unit",
            "steps-0-stepDescription": "Mix ingredients",
            "pictFile": (io.BytesIO(b""), ""),
            "action_button": "post"
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )

    assert response.status_code == 200

    # check that it posted
    postedRecipe = db.session.get(Recipe, draft.id)
    assert postedRecipe.is_draft is False
    assert postedRecipe.title == "Simple Mix"

    # check redirect to main page
    assert b"Welcome" in response.data

    do_logout(test_client, path='/user/logout')