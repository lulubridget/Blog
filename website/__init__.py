from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "helloworld"
    #link to app.py

    ##link to db, the sqlite will do the user query, so no need to write yourself
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # dot here mean relative import, from same python package(website). use when import module from sane part
    # without dot, is absolute import:specifies the full path. use when import package
    # from different parts of project
    from .views import views
    from .auth import auth
    #register the blueprint, url_prefix allows to specify a URL prefix for all the routes defined in the blueprint.
    #if put url_prefix ="/api"here, all url in views.py, need to add "api/".
    app.register_blueprint(views, url_prefix ="/")
    app.register_blueprint(auth, url_prefix = "/")

    from .models import User, Post

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    #login_manager check the session see are you already logged in
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("created database!")
