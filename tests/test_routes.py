"""
This file contains the functional tests for the main.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
import pytest
from app import create_app, db
from app.main.models import Ingredient, User, Tag, Recipe, RecipeIngredientUse, RecipeStep
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

def new_user(first_name, last_name, username, email, password, certified=False):
    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        is_certified = certified,
        )
    user.set_password(password)
    return user

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
    # Create the database and the database table
    db.create_all()
    # initialize the tags
    init_tags()
    #add a user    
    user1 = new_user(first_name='Cooking', last_name='Mama', username='CookingMama', email='cookingmama@wpi.edu', password='123')
    # Insert user data
    db.session.add(user1)
    # Commit the changes for the users
    db.session.commit()

    # add a couple ingredients
    i1 = Ingredient(name="avocado")
    db.session.add(i1)
    i2 = Ingredient(name="bread")
    db.session.add(i2)
    db.session.commit()

    # add a recipe
    r1 = Recipe(title = "Avocado Toast", description = "A delicious and easy breakfast", servingSize = 1, estimatedHrs = 0, estimatedMins = 15, is_draft=False, user_id=user1.id)
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

def test_recommended_recipes(test_client,init_database): # rewrite this test
    """
    GIVEN a Flask application configured for testing , after user logs-in,
    THEN check that response is valid and the recommended recipes are updated in the database
    """
    # login
    # do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    # #first post two smile stories
    # all_tags = db.session.scalars(sqla.select(Tag)).all()
    # tags1 = list( map(lambda t: t.id, all_tags[:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    # response = test_client.post('/post', 
    #                       data=dict(title='My test post', body='This is my first test post.',happiness_level=2, tag = tags1),
    #                       follow_redirects = True)
    # assert response.status_code == 200
    # post1 = db.session.scalars(sqla.select(Post).where(Post.title =='My test post')).first()
    # assert post1 is not None #There should be at least one post with body "My test post"

    # tags2 = list( map(lambda t: t.id, all_tags[1:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    # response = test_client.post('/post', 
    #                       data=dict(title='Second post', body='Here is another post.',happiness_level=1, tag = tags2),
    #                       follow_redirects = True)
    # assert response.status_code == 200
    # post2 = db.session.scalars(sqla.select(Post).where(Post.body =='Here is another post.')).first()
    # assert post2 is not None  #There should be at least one post with body "Here is another post."

    # #there should be total two posts
    # all_posts = db.session.scalars(sqla.select(Post)).all()
    # assert len(all_posts) == 2

    # #like the second post 
    # response = test_client.post('/post/'+str(post2.id)+'/like', 
    #                       data={},
    #                       follow_redirects = True)
    # assert response.status_code == 200
    # #Will return the updated count as JSON
    # data = eval(response.data)
    # assert data['post_id'] == post2.id
    # assert data['like_count'] == 1
    # #check whether the likecount was updated successfully
    # first_post = db.session.get(Post, post1.id)
    # assert first_post.likes == 0 
    # second_post = db.session.get(Post, post2.id)
    # assert second_post.likes == 1  

    #finally logout
    # do_logout(test_client, path = '/user/logout')    
    pass

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
    assert b"Avocado Toast" in response.data
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
    # check redirect
    assert b"Welcome!" in response.data
    # check flash message
    assert b"Error: could not find recipe" in response.data
    
    # finally logout
    do_logout(test_client, path = '/user/logout') 
    pass

def test_recipe_step_operations(test_client, init_database):
    # Note: this test was generated by ChatGPT using the formats of previous tests and then modified and additionally commented
    do_login(test_client, path='/user/login', username='CookingMama', passwd='123')

    # Create draft
    test_client.post('/recipe/create', data={"select_button": "new"}, follow_redirects=True)
    draft = db.session.scalars(sqla.select(Recipe).where(Recipe.is_draft == True)).first()
    assert draft is not None

    # -------------------------
    # ADD STEP
    # -------------------------
    response = test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "title": "Step Test",
            "description": "",
            "servingSize": 1,
            "estimatedHrs": 0,
            "estimatedMins": 0,
            "tags": [],
            "ingredients": [],
            "steps-0-stepDescription": "First step",
            "steps-1-stepDescription": "Second step",
            "action_button": "add",
            "pictFile": (io.BytesIO(b""), "")
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )
    assert response.status_code == 200
    # check that the steps appear
    assert b"First step" in response.data
    assert b"Second step" in response.data

    steps = db.session.scalars(
        sqla.select(RecipeStep).where(RecipeStep.recipe_id == draft.id)
    ).all()

    assert len(steps) == 2

    # -------------------------
    # MOVE STEP DOWN
    # -------------------------
    first_step = sorted(steps, key=lambda s: s.stepNum)[0]
    test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "step_down_button": str(first_step.id),
            "pictFile": (io.BytesIO(b""), "")
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )
    db.session.refresh(first_step)
    assert first_step.stepNum == 2

    # -------------------------
    # MOVE STEP UP
    # -------------------------
    test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "step_up_button": str(first_step.id),
            "pictFile": (io.BytesIO(b""), "")
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )

    db.session.refresh(first_step)
    assert first_step.stepNum == 1

    # -------------------------
    # REMOVE STEP
    # -------------------------
    test_client.post(
        f'/recipe/{draft.id}/edit',
        data={
            "step_remove_button": str(first_step.id),
            "pictFile": (io.BytesIO(b""), "")
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )

    deleted_step = db.session.get(RecipeStep, first_step.id)
    assert deleted_step is None

    do_logout(test_client, path='/user/logout')

def test_recipe_ingredient_operations(test_client, init_database):
    # Note: this test was generated by ChatGPT using the formats of previous tests and then modified and additionally commented
    do_login(test_client, path='/user/login', username='CookingMama', passwd='123')

    # Ensure ingredient exists
    ingredient = db.session.scalars(
        sqla.select(Ingredient)
    ).first()

    if ingredient is None:
        ingredient = Ingredient(name="flour")
        db.session.add(ingredient)
        db.session.commit()

    # Create draft
    test_client.post(
        '/recipe/create',
        data={"select_button": "new"},
        follow_redirects=True
    )

    draft = db.session.scalars(
        sqla.select(Recipe).where(Recipe.is_draft == True)
    ).first()

    # -------------------------
    # ADD INGREDIENT
    # -------------------------
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

    uses = db.session.scalars(
        sqla.select(RecipeIngredientUse).where(
            RecipeIngredientUse.recipe_id == draft.id
        )
    ).all()

    assert len(uses) == 1

    # -------------------------
    # REMOVE INGREDIENT
    # -------------------------
    ing_use = uses[0]

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
            "action_button": str(ingredient.id),
            "pictFile": (io.BytesIO(b""), "")
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
            RecipeIngredientUse.ingredient_id == ing_use.ingredient_id
        )
    ).first()
    assert deleted_use is None

    do_logout(test_client, path='/user/logout')


