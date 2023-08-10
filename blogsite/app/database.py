from os import path
from . import db
def create_database(app,DB_NAME):
    if not path.exists("app/"+DB_NAME):
        with app.app_context():
            db.create_all()