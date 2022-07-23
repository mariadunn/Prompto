from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jsglue import JSGlue
from flask_ckeditor import CKEditor

convention = { # this is something to do with SQLAlchemy
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention) # ^
db = SQLAlchemy(metadata=metadata) # ^
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
jsglue = JSGlue()
ckeditor = CKEditor()

def create_app(config_class=Config):

    app = Flask(__name__, static_folder='static')
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True) # last bit not in tutorial
    login.init_app(app)
    jsglue.init_app(app)
    ckeditor.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)


    return app

from app import models
