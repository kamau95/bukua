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


    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    

    @app.context_processor
    def inject_user():
        return dict(user=current_user)


    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('username')}:{os.getenv('password')}@{os.getenv('hostname')}/{os.getenv('database_name')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    #initialize sqlalchemy
    db.init_app(app)


    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Initialize Flask-CORS
    CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})


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
