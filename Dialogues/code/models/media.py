from db import db

class MediaModel(db.Model):
    
    __tablename = 'medias'  
    id = db.column(db.Integer, primary_key = True )
    name = db.column(db.String(80))

    def __init__(self, name):
        self.name = name
   
    def save_to_db(self, name):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'id'   : self.id, 
                'name' : self.name }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()