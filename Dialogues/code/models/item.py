from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id            = db.Column(db.Integer, primary_key=True)
    creator_id    = db.Column(db.Integer, ForeignKey("creator.id"))
    media_id      = db.Column(db.Integer, ForeignKey("media.id"))
    category_id   = db.Column(db.Integer, ForeignKey("category.id"))
    EAN           = db.Column(db.Integer)
    ASIN          = db.Column(db.Integer)    
    name          = db.Column(db.String(80))    
    synopsys      = db.Column(db.String(500))
    creation_date = db.Column(db.datetime)

    def __init__(self, creator_id, media_id, category_id,EAN,ASIN,name,synopsys):
        self.creator_id = creator_id
        self.media_id = media_id
        self.category_id = category_id
        
        self.EAN = EAN
        self.ASIN = ASIN    

        self.name = name
        self.synopsys = synopsys
        self.creation_date = datetime.now()

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
                 'creation_date':self.creation_date
               }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()        

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name ).first() 

    @classmethod
    def find_by_EAN(cls, EAN):
        return cls.query.filter_by(EAN=EAN).first()     

    @classmethod
    def find_by_ASIN(cls, ASIN):
        return cls.query.filter_by(ASIN=ASIN).first()  