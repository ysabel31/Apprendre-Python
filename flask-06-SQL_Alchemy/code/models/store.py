from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    store = db.relationship('ItemModel', lazy = 'dynamic')

    def __init__(self, name):
        self.name  = name
        
    def json(self):
        return { 'name' : self.name, 'items':self.items.all()}
        
    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() 
        # Select * from items where name = name LIMIT 1 
    
    def save_to_db(self):
        # Session in this instance is a collection of objects 
        # that we are going to write to the database
        # we can add multiple objects to the session and then write mutiple at once
        # in this case one
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()