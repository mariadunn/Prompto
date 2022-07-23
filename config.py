import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' #TODO: change

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Image Upload config

    MAX_CONTENT_LENGTH = 1024 * 1024 # 1024 = 1mb
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
    UPLOAD_PATH = 'app/static/uploads'
