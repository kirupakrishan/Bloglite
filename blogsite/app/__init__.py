from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

cur_dir = path.abspath(path.dirname(__file__))
db = SQLAlchemy()
DB_NAME = 'database.db'
IMG_FOLDER="static/img"
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld'
    app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+path.join(cur_dir,DB_NAME)
    app.config["IMG_FOLDER"]=IMG_FOLDER
    db.init_app(app)
    app.app_context().push
    from .views import views
    from .auth import auth
    from .controllers import ctrl
    from .database import create_database

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(ctrl,url_prefix='/')

    from .models import User
    create_database(app,DB_NAME)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

