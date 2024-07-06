from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_login import current_user
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from os import path
from flask_migrate import Migrate




# Import the db object from models
from .models import db, User


def create_app():
    load_dotenv()  # Load environment variables from .env file

    database_uri = os.getenv('DATABASE_URI')
    secret_key = os.getenv('SECRET_KEY')
    tmdb_api_key = os.getenv('TMDB_API_KEY')

    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['DEBUG'] = False
    #app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true' 

    @app.context_processor
    def inject_user():
        return dict(user=current_user)


    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # SSL configuration
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'ssl': {
            'ca': 'certs/ca.cert'
        }
      }
    }

    #initialize sqlalchemy
    db.init_app(app)


    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Initialize Flask-CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Create all tables
    with app.app_context():
        db.create_all()


    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))


    #register blueprints
    from .auth import auth as auth_blueprint
    from .views import views as views_blueprint
    app.register_blueprint(auth_blueprint, url_prefix=('/'))
    app.register_blueprint(views_blueprint, url_prefix=('/'))


    # Teardown session
    @app.teardown_appcontext
    def remove_session(exception=None):
        db.session.remove()

    return app
