#! /usr/local/bin/python3 
# First python run the import file 
# in order to make sure that every thing is in order
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_restful_swagger import swagger

from security import authenticate, identity
from resources.user import User, UserList, UserRegister
from resources.category import Category, CategoryList
from resources.creator import Creator, CreatorList
from resources.media import Media, MediaList
from resources.item import Item, ItemList
from models.item import ItemModel


#jsonify is a method not a class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dialogues.db'

# turn off the Flask SQLAlchemy modification tracker 
# it does not turn off the SQLAlchemy modification tracker 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key= 'Breizh_or_not_Breizh'

# set the location for the whoosh index
app.config['WHOOSHEE_DIR'] = '../whoosh_index'

#api = Api(app)
# Wrapp API
api = swagger.docs(Api(app), apiVersion='0.1',
                             basePath='http://localhost:5000',
                             resourcePath='/',
                             produces=["application/json", "text/html"],
                             api_spec_url='/api/spec',
                             description='Dialogues API')

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(User,'/user/<int:_id>')
api.add_resource(UserRegister, '/user/register') 
api.add_resource(UserList, '/user')

api.add_resource(Category,'/category/<int:_id>')
api.add_resource(CategoryList, '/category')

api.add_resource(Creator,'/creator/<int:_id>')
api.add_resource(CreatorList, '/creator')

api.add_resource(Media,'/media/<int:_id>')
api.add_resource(MediaList, '/media')

api.add_resource(Item,'/item/<int:_id>')
api.add_resource(ItemList, '/item')
#api.add_resource(Media, '/media') 

# __main__ is the special name assign by python for the file we run
# allow us to not execute app.run if app.py is imported into another program
if __name__ == '__main__':
   from db import db,whooshee
   with app.app_context():
       db.init_app(app) 
       db.create_all()
       whooshee.init_app(app)
       whooshee.reindex()

   app.run(port=5000, debug = True)