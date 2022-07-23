# THIS FILE CREATES THE BLUEPRINT FOR 'MAIN', i.e. THE GENERAL FUNCTIONALITY OF THE APP #

from flask import Blueprint # gets the Blueprint functionality from flask

bp = Blueprint('main', __name__, template_folder='templates') # Constructs a blueprint for Main, and specifies where the templates are coming from (main/templates)

from app.main import routes
