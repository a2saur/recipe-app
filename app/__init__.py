from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
oauth = OAuth()

migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 2. Initialize the extension with the app
    oauth.init_app(app)


    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER_MAIN
    app.config['UPLOAD_FOLDER'] = config_class.IMG_UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 250 * 1024

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app, db)
    moment.init_app(app)
    mail.init_app(app)

    # 3. REGISTER THE CLIENT HERE
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    
    # blueprint registration
    from app.main import main_blueprint as main
    main.template_folder = Config.TEMPLATE_FOLDER_MAIN
    app.register_blueprint(main)

    from app.auth import auth_blueprint as auth
    auth.template_folder = Config.TEMPLATE_FOLDER_AUTH
    app.register_blueprint(auth)

    from app.user import user_blueprint as user
    user.template_folder = Config.TEMPLATE_FOLDER_USER
    app.register_blueprint(user)

    from app.recipe import recipe_blueprint as recipe
    recipe.template_folder = Config.TEMPLATE_FOLDER_RECIPE
    app.register_blueprint(recipe)

    from app.cookbook import cookbook_blueprint as cookbook
    cookbook.template_folder = Config.TEMPLATE_FOLDER_COOKBOOK
    app.register_blueprint(cookbook)

    from app.errors import error_blueprint as errors
    errors.template_folder = Config.TEMPLATE_FOLDER_ERRORS
    app.register_blueprint(errors)

    return app
