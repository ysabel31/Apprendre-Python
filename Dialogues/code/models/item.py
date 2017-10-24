from flask_restful_swagger import swagger
from db import db,whooshee
import datetime
from whoosh.analysis import StemmingAnalyzer

item_creator = db.Table('item_creator',
    db.Column('item_id',    db.Integer, db.ForeignKey('items.id'), primary_key=True),
    db.Column('creator_id', db.Integer, db.ForeignKey('creators.id'), primary_key=True)
)
@whooshee.register_model('name', 'synopsys')
@swagger.model
class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id                = db.Column(db.Integer, primary_key=True)    
    item_creators     = db.relationship(
        'CreatorModel', 
        secondary = item_creator, 
        backref = db.backref('creator_items',lazy='dynamic')
    )
    media_id          = db.Column(db.Integer, db.ForeignKey("media.id"))
    category_id       = db.Column(db.Integer, db.ForeignKey("categories.id"))
    EAN               = db.Column(db.Integer)
    ASIN              = db.Column(db.Integer)    
    ASIN_LINK_AMAZON  = db.Column(db.String(1024))
    name              = db.Column(db.String(80))    
    synopsys          = db.Column(db.String(1024))
    creation_date     = db.Column(db.DateTime)
    modification_date = db.Column(db.DateTime)
    
    def __init__(self, 
                 _creator_id, 
                 media_id, 
                 category_id, 
                 EAN               = None,                  
                 ASIN              = None, 
                 ASIN_LINK_AMAZON  = None, 
                 name              = None, 
                 synopsys          = None,
                 modification_date = None):
        from models.creator import CreatorModel
        for creator_id in _creator_id:
            print(creator_id)
            Creator= CreatorModel.find_by_id(creator_id)
            self.item_creators.append(Creator)
        self.media_id          = media_id
        self.category_id       = category_id
        
        self.EAN               = EAN
        self.ASIN              = ASIN    
        self.ASIN_LINK_AMAZON  = ASIN_LINK_AMAZON

        self.name              = name
        self.synopsys          = synopsys
        self.creation_date     = datetime.datetime.now()
        self.modification_date = datetime.datetime.now()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()    
    
    def json(self):
        item_creators = []
        for creator in self.item_creators:
            item_creators.append(creator.id)

        return { 'id'               : self.id, 
                 'item_creators'    : item_creators,
                 'media_id'         : self.media_id,
                 'category_id'      : self.category_id,
                 'EAN'              : self.EAN,
                 'ASIN'             : self.ASIN,
                 'ASIN_LINK_AMAZON' : self.ASIN,
                 'name'             : self.name,
                 'synopsys'         : self.synopsys,
                 'creation_date'    : self.creation_date.isoformat(),
                 'modification_date': self.creation_date.isoformat()
               }

    def save_to_db(self):
        db.session.add(self)        
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()        

    @classmethod
    def find_text(cls,text):
        print(text)
        return cls.query.whooshee_search(text).all()    

    @classmethod
    def find(cls,
             _creator_id  = None, 
             media_id    = None, 
             category_id = None, 
             EAN         = None,                  
             ASIN        = None, 
             name        = None, 
             strict      = None):

        filters = []

        from models.creator import CreatorModel
        if _creator_id:
            filters.append(CreatorModel.id == _creator_id)

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
                return cls.query.join(ItemModel.item_creators).filter(*filters).all()
        else: 
            return cls.query.all()