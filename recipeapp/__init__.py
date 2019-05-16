from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from recipeapp.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import logging


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    from recipeapp.main.routes import main
    from recipeapp.users.routes import users
    from recipeapp.recipes.routes import recipes
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(recipes)

    return app
