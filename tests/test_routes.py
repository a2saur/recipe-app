"""
This file contains the functional tests for the main.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
from datetime import datetime
import os
from time import timezone
import pytest
from app import create_app, db
from app.main.models import Ingredient, Recipe, RecipeIngredientUse, RecipeStep, User, Tag
from config import Config
import sqlalchemy as sqla


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
             certified=False, allergies=None, dietary_tags=None, preferred_tags=None):

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
                    'Bread', 'Flour', 'Sugar', 'Salt', 'Pepper', 'Pasta', 'Parmesan']
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
                     allergies=[peanut_allergy], dietary_tags=[vegan_tag], preferred_tags=[easy_tag, breakfast_tag])
    # Insert user data
    db.session.add(user1)

    # Add a recipe for the user

    # Commit the changes for the users
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
    # Login as CookingMama
    do_login(test_client, path = '/user/login', username = 'CookingMama', passwd = '123')
    
    # # Post two recipes with different tags and check that they are recommended correctly based on the user's preferred tags and dietary restrictions
    # r0 = Recipe(title = "Corn Soup", description = "Known in Japan as \"corn potage\", this recipe is made from corn kernels cut from the cob. The soup becomes very smooth and strained after cooking, creating a thick paste-like texture, similar to seafood bisque.", servingSize = 1, estimatedHrs = 0, estimatedMins = 45, is_draft=False, user_id=test_client.id)
    # r0.timestamp = datetime.now(timezone.utc)
    # r0.pictFile = "207add98-112c-11f1-a181-1ebf2a7aaad6_cooking-mama-corn-potage.png"
    # db.session.add(r0)

    # r1 = Recipe(title = "Avocado Toast", description = "Guacamole spread topped with chilis!", servingSize = 1, estimatedHrs = 0, estimatedMins = 15, is_draft=False, user_id=u1.id)
    # r1.timestamp = datetime.now(timezone.utc)
    # r1.pictFile = "2b117cbc-112c-11f1-a181-1ebf2a7aaad6_cooking-mama-avocado-toast.png"
    # db.session.add(r1)
    # db.session.commit()

    # # Get tags 
    # vegan_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'vegan')).first()
    # easy_tag = db.session.scalars(sqla.select(Tag).where(Tag.name == 'easy')).first()

    # # Add recipe steps
    # s00 = RecipeStep(stepNum = 1, description = "Finely dice it", recipe_id = r0.id)
    # db.session.add(s00)
    # s01 = RecipeStep(stepNum = 2, description = "Cut corn from cob", recipe_id = r0.id)
    # db.session.add(s01)
    # s02 = RecipeStep(stepNum = 3, description = "Spread the butter", recipe_id = r0.id)
    # db.session.add(s02)
    # s03 = RecipeStep(stepNum = 4, description = "Stir fry it", recipe_id = r0.id)
    # db.session.add(s03)
    # s04 = RecipeStep(stepNum = 5, description = "Boil it", recipe_id = r0.id)
    # db.session.add(s04)
    # s05 = RecipeStep(stepNum = 6, description = "Use the mixer", recipe_id = r0.id)
    # db.session.add(s05)
    # s06 = RecipeStep(stepNum = 7, description = "Strain", recipe_id = r0.id)
    # db.session.add(s06)
    # s07 = RecipeStep(stepNum = 8, description = "Boil it", recipe_id = r0.id)
    # db.session.add(s07)
    # db.session.commit()

    # # Add ingredients to the recipe
    # onion = Ingredient(name='Onion')
    # db.session.add(onion)
    # cream = Ingredient(name='Cream')
    # db.session.add(cream)
    # corn = Ingredient(name='Corn')
    # db.session.add(corn)
    # db.session.flush()
    # ri00 = RecipeIngredientUse(recipe_id = r0.id, ingredient_id = onion.id, amount = 0.5, unit = "unit")
    # db.session.add(ri00)
    # ri01 = RecipeIngredientUse(recipe_id = r0.id, ingredient_id = cream.id, amount = 1, unit = "unit")
    # db.session.add(ri01)
    # ri02 = RecipeIngredientUse(recipe_id = r0.id, ingredient_id = corn.id, amount = 4, unit = "tbsp")
    # db.session.add(ri02)
    # db.session.commit()
    


    # response = test_client.post('/recipe/create', data={
    #                         'title': 'Sunny',
    #                         'pictFile': '207add98-112c-11f1-a181-1ebf2a7aaad6_cooking-mama-corn-potage.png',
    #                         'description': 'Known in Japan as \"corn potage\", this recipe is made from corn kernels cut from the cob. The soup becomes very smooth and strained after cooking, creating a thick paste-like texture, similar to seafood bisque.',
    #                         'servingSize': 1,
    #                         'estimatedHrs': 0,
    #                         'estimatedMins': 45,
    #                         'tags': [vegan_tag.id, easy_tag.id],  # This triggers the redirect logic
    #                         'ingredients': [vegan_tag.id],
    #                         'steps': 
    #                     },
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

    # #finally logout
    # do_logout(test_client, path = '/user/logout')    
    pass

# ------------------------------------
# RECIPE ROUTES TESTS

def test_post_recipe(test_client,init_database): # rewrite this test
    """
    GIVEN a Flask application configured for testing , after user logs in,
    WHEN the '/post' page is requested (GET)  AND PostForm' form is submitted (POST)
    THEN check that response is valid and the class is successfully created in the database
    """
    # #login
    # do_login(test_client, path = '/user/login', username = 'snow', passwd = '1234')
    
    # #test the "post" form 
    # response = test_client.get('/post')
    # assert response.status_code == 200
    # assert b"Post New Smile" in response.data
    
    # all_tags = db.session.scalars(sqla.select(Tag)).all()
    # #test posting a smile story
    # tags1 = list( map(lambda t: t.id, all_tags[:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    # response = test_client.post('/post', 
    #                       data=dict(title='My test post', body='This is my first test post.',happiness_level=2, tag = tags1),
    #                       follow_redirects = True)
    # #checking the page content after redirect
    # assert response.status_code == 200
    # assert b"Welcome to Smile Portal!" in response.data
    # assert b"My test post" in response.data 
    # assert b"This is my first test post." in response.data 

    # #checking whether the database is updated correctly with the post request 
    # thepost = db.session.scalars(sqla.select(Post).where(Post.title =='My test post')).first()
    # tags_of_post = thepost.get_tags()
    # assert (len(tags_of_post))== 3 #should have 3 tags
    # assert all_tags[0] in tags_of_post  #first tag should be one of the tags of the post. 
    
    # tags2 = list( map(lambda t: t.id, all_tags[1:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    # response = test_client.post('/post', 
    #                       data=dict(title='Second post', body='Here is another post.',happiness_level=1, tag = tags2),
    #                       follow_redirects = True)
    # #checking the page content after redirect  
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




    
