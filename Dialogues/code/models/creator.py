from db import db
from flask_restful_swagger import swagger

@swagger.model
class CreatorModel(db.Model):
    __tablename__ = 'creators'

    id = db.Column(db.Integer, primary_key=True)
    
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))

    def __init__(self, lastname, firstname=None):
        if firstname:
            self.firstname = firstname
        if lastname:    
            self.lastname = lastname

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()    
    
    def json(self):
        return { 'id':self.id, 'firstname' : self.firstname, 'lastname':self.lastname}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()        

    @classmethod
    def find_by_lastname(cls, lastname):
        #users = User.query.filter(func.soundex(User.name) == func.soundex('Tina')).all()
        return cls.query.filter(db.func.soundex(CreatorModel.lastname) == db.func.soundex(lastname)).first()

    @classmethod
    def find(cls, lastname=None, firstname=None):
        filters = []

        if lastname:
            filters.append(db.func.soundex(CreatorModel.lastname) == db.func.soundex(lastname))
        if firstname:
            filters.append(db.func.soundex(CreatorModel.firstname) == db.func.soundex(firstname))        

        if len(filters) > 0:    
            return cls.query.filter(*filters).all()
        else: 
            return cls.query.all()
