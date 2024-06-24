from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
from os import path


# Import the db object from models
from .models import db, User


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'nikubayaman'


    # MySQL Configuration
    username = 'kamau'
    password = 'soft%40402'
    hostname = 'localhost'  # or your database server's address
    database_name = 'movie_search'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{hostname}/{database_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    #initialize sqlalchemy
    db.init_app(app)


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
