#! /usr/local/bin/python3 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from db              import db
from models.item     import ItemModel
from models.media    import MediaModel   
from models.creator  import CreatorModel
from models.category import CategoryModel
from models.user     import UserModel

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)

migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()