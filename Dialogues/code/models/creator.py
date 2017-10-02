from db import db

class CreatorModel(db.Model):
    __tablename__ = 'creators'

    id = db.Column(db.Integer, primary_key=True)
    
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))

    def __init__(self, firstname,lastname):
        self.firstname = firstname
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
        return cls.query.filter_by(lastname=lastname).first()

    @classmethod
    def find_by_name(cls, lastname, firstname):
        return cls.query.filter_by(firstname=firstname,lastname=lastname ).first() 
