import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'meal_planner.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SSO Credentials
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    ROOT_PATH = basedir
    STATIC_FOLDER = os.path.join(basedir, 'app//static')
    TEMPLATE_FOLDER_MAIN = os.path.join(basedir, 'app//main//templates')
    TEMPLATE_FOLDER_ERRORS = os.path.join(basedir, 'app//errors//templates')
    TEMPLATE_FOLDER_AUTH = os.path.join(basedir, 'app//auth//templates')    
    TEMPLATE_FOLDER_USER = os.path.join(basedir, 'app//user//templates')
    TEMPLATE_FOLDER_RECIPE = os.path.join(basedir, 'app//recipe//templates')
    TEMPLATE_FOLDER_COOKBOOK = os.path.join(basedir, 'app//cookbook//templates')
    IMG_UPLOAD_FOLDER = os.path.join(basedir, 'app//static//img//recipe-imgs')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'mealplanner.sender@gmail.com'
    MAIL_PASSWORD = 'wbfnppbtdwzawbxf'

    ADMINS = ['mealplanner.sender@gmail.com']