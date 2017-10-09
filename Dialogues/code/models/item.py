from db import db
import datetime

class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id            = db.Column(db.Integer, primary_key=True)
    creator_id    = db.Column(db.Integer, db.ForeignKey("creators.id"))
    media_id      = db.Column(db.Integer, db.ForeignKey("media.id"))
    category_id   = db.Column(db.Integer, db.ForeignKey("categories.id"))
    EAN           = db.Column(db.Integer)
    ASIN          = db.Column(db.Integer)    
    name          = db.Column(db.String(80))    
    synopsys      = db.Column(db.String(1024))
    creation_date = db.Column(db.DateTime)

    def __init__(self, 
                 creator_id, 
                 media_id, 
                 category_id, 
                 EAN = None,                  
                 ASIN = None, 
                 name = None, 
                 synopsys = None):

        self.creator_id  = creator_id
        self.media_id    = media_id
        self.category_id = category_id
        
        self.EAN = EAN
        self.ASIN = ASIN    

        self.name = name
        self.synopsys = synopsys
        self.creation_date = datetime.datetime.now()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()    
    
    def json(self):
        return { 'id':self.id, 
                 'creator_id' : self.creator_id,
                 'media_id' : self.media_id,
                 'category_id' : self.category_id,
                 'EAN' : self.EAN,
                 'ASIN' : self.ASIN,
                 'name':self.name,
                 'synopsys':self.synopsys,
                 'creation_date':self.creation_date.isoformat()
               }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()        

    @classmethod
    def find(cls,
             creator_id = None, 
             media_id = None, 
             category_id = None, 
             EAN = None,                  
             ASIN = None, 
             name = None, 
             strict= None):

        filters = []

        if creator_id:
            filters.append(ItemModel.creator_id == creator_id)

        if media_id:
            filters.append(ItemModel.media_id == media_id)        

        if category_id:
            filters.append(ItemModel.category_id == category_id)

        if EAN:
            filters.append(ItemModel.EAN == EAN)        

        if ASIN:
            filters.append(ItemModel.ASIN == ASIN)        

        if name:
            if strict:
                filters.append(ItemModel.name == name)            
            else:    
                filters.append(db.func.soundex(ItemModel.name) == db.func.soundex(name))            

        if len(filters) > 0:    
            return cls.query.filter(*filters).all()
        else: 
            return cls.query.all()