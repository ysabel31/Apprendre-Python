from db import db

class MediaModel(db.Model):
    __tablename__ = 'media'  
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80))

    def __init__(self, category):
        self.category = category
   
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id'   : self.id, 
                'category' : self.category }

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category).first()

    @classmethod
    def find(cls,category=None):
        if category:
            return cls.query.filter_by(category=category).all()
        return cls.query.all()    
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()