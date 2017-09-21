# First python run the import file 
# in order to make sure that every thing is in order
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

#jsonify is a method not a class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# turn off the Flask SQLAlchemy modification tracker 
# it does not turn off the SQLAlchemy modification tracker 
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key= 'asdf'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/piano
api.add_resource(ItemList, '/items') 
api.add_resource(UserRegister, '/register') 

# __main__ is the special name assign by python for the file we run
# allow us to not execute app.run if app.py is imported into another program
if __name__ == '__main__':
   from db import db
   db.init_app(app) 
   app.run(port=5000, debug = True)