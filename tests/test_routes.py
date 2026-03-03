"""
This file contains the functional tests for the main.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
from turtle import title
from time import timezone
import pytest
from app import create_app, db
from app.main.models import Ingredient, User, Tag, Recipe, Cookbook, RecipeIngredientUse, RecipeStep
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
    # #login
    # do_login(test_client, path = '/user/login', username = 'snow', passwd = '1234')
    
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

# ------------------------------------
# COOKBOOK ROUTES TESTS
def test_create_cookbook(test_client,init_database):
    user = db.session.scalars(sqla.select(User).where(User.username == 'CookingMama')).first()
    assert user is not None
    user.is_certified = True
    db.session.commit()
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
    assert b"At least one recipe must be selected!" in response.data
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
