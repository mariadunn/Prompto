import os
from pathlib import Path


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' #TODO: change

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    _project_root = Path(__file__).resolve().parent.parent
    _default_sqlite_db = _project_root / "database.db"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
    'postgres://', 'postgresql://') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')


    # Image Upload config

    MAX_CONTENT_LENGTH = 1024 * 1024 # 1024 = 1mb
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
    UPLOAD_PATH = 'app/static/uploads'
