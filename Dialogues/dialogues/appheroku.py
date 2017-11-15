#! /usr/local/bin/python3 
# First python run the import file 
# in order to make sure that every thing is in order
from app import app
from db import db

db.init_app(app) 

@app.before_first_request
def create_tables():
    db.create_all()