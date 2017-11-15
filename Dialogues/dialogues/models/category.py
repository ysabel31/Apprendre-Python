from db import db
from flask_restful_swagger import swagger

@swagger.model
class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()    
    
    def json(self):
        return { 'id':self.id, 'name' : self.name}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find(cls, name=None):
        if name:
            return cls.query.filter_by(name=name).all()        
        return cls.query.filter_by().all()   

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()        

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name ).first() 
