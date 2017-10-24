from flask_restful import Resource
from flask_restful_swagger import swagger

from webargs import fields
from webargs.flaskparser import use_args
from models.item import ItemModel
import datetime

class Item(Resource):
    "Item Resource"
    args_required = {
            'creator_id'    : fields.List(fields.Integer(required=True,
                                                             error_messages = {"required":"Creator id cannot be blank"})),
            'media_id'      : fields.Integer(required=True,
                                             error_messages = {"required":"Media id cannot be blank"}),
            'category_id'   : fields.Integer(required=True,
                                             error_messages = {"required":"Category id cannot be blank"}),
            'EAN'           : fields.Integer(),
            'ASIN'          : fields.Integer(),
            'ASIN_LINK_AMAZON'          : fields.String(),
            'name'          : fields.String(required=True,
                                            error_messages = {"required":"Name cannot be blank"}),
            'synopsys'      : fields.String(required=False),
            'creation_date' : fields.DateTime(required=False),
    }

    #GET
    @swagger.operation(
        notes='Get an item by ID',
        responseClass = ItemModel.__name__,
        nickname      = 'get',
        parameters    = [
            {
              "name": "_creator_id",
              "description": "Item id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            }
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Item found"
            },
            {
              "code": 404,
              "message": "Item not found"
            }
        ]
    )
    def get(self, _id):
        item = ItemModel.find_by_id(_id)
        if item:
            return item.json(), 200
        else:
            return{"message":"Item id not found"}, 404

    # DELETE        
    @swagger.operation(
        notes='Delete an item by id',
        responseClass = ItemModel.__name__,
        nickname      = 'delete',
        parameters    = [
            {
              "name": "_id",
              "description": "Item id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            }
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Item deleted"
            },
            {
              "code": 404,
              "message": "Item to delete not found"
            }
        ]
    )        
    def delete(self, _id):
        item = ItemModel.find_by_id(_id)
        
        if item:
            item.delete_from_db()
            return {'message': "item id {} has been deleted".format(item.id)},200        

        return {'message': "No item id {} to delete".format(item.category)},200        

    # PUT
    @swagger.operation(
        notes='Update an item, id is required',
        responseClass = [ItemModel.__name__],
        nickname      = 'put',
        parameters    = [
            {
              "name": "_id",
              "description": "Item id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            },
            {
              "name": "creator_id",
              "description": "Creator id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            },
            {
              "name": "media_id",
              "description": "Media id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            },
            {
              "name": "category_id",
              "description": "Category id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            },
            {
              "name": "EAN",
              "description": "EAN",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "form"
            },
            {
              "name": "ASIN",
              "description": "ASIN",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "form"
            },
            {
              "name": "ASIN_LINK_AMAZON",
              "description": "A link to Amazon regarding this item",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            },
            {
              "name": "name",
              "description": "Item name",
              "required": True,
              "allowMultiple": False,
              "dataType": "String",
              "paramType": "form"
            },
            {
              "name": "synopsis",
              "description": "Item synopsis",
              "required": True,
              "allowMultiple": False,
              "dataType": "String",
              "paramType": "form"
            },
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Creator updated"
            },
            {
              "code": 400,
              "message": "Creator to update not found"
            }
        ]
    )              
    @use_args(args_required)         
    def put(self, args,_id):
        item = ItemModel.find_by_id(_id)
        if item:   
            from models.creator import CreatorModel
            for creator in args['creator_id']:
              Creator= CreatorModel.find_by_id(creator)
              item.item_creators.append(Creator)
                    #TODO: Boucle comme dans le model 
            #item.creator_id   =  args['creator_id']                   
            item.media_id     =  args['media_id']                   
            item.creator_id   =  args['category_id']                   
            item.EAN          =  args['EAN']                   
            item.ASIN         =  args['ASIN']  
            item.ASIN_LINK_AMAZON         =  args['ASIN_LINK_AMAZON']                   
            item.name         =  args['name']                  
            modification_date = datetime.datetime.now()             
            item.save_to_db()    
            return {"message":"Creator {} has been updated".format(_id)}, 200
            
        return{"message":"Creator id {} doesn't exists".format(_id)}, 400 # media to update not found   


class ItemList(Resource):    
    args_required = {
            '_creator_id'        : fields.List(fields.Integer(required=True,
                                                             error_messages = {"required":"Creator id cannot be blank"})),
            'media_id'          : fields.Integer(required=True,
                                                 error_messages = {"required":"Media id cannot be blank"}),
            'category_id'       : fields.Integer(required=True,
                                                 error_messages = {"required":"Category id cannot be blank"}),
            'EAN'               : fields.Integer(required=False),
            'ASIN'              : fields.Integer(required=False),
            'ASIN_LINK_AMAZON'  : fields.String(required=False),
            'name'              : fields.String(required=True,
                                                error_messages = {"required":"Name cannot be blank"}),
            'synopsys'          : fields.String(required=False),
            'creation_date'     : fields.DateTime(required=False),
            'modification_date' : fields.DateTime(required=False),
    }

    args_optional = {
            '_creator_id'       : fields.Integer(required=False),
            'media_id'          : fields.Integer(required=False),
            'category_id'       : fields.Integer(required=False),
            'EAN'               : fields.Integer(required=False),
            'ASIN'              : fields.Integer(required=False),
            'ASIN_LINK_AMAZON'  : fields.String(required=False),
            'name'              : fields.String(required=False),
            'synopsys'          : fields.String(required=False),
            'creation_date'     : fields.DateTime(required=False),
            'modification_date' : fields.DateTime(required=False),
            'text'              : fields.String(required=False), 
    }
    # GET      
    @swagger.operation(
        notes='Get an items list',
        responseClass = [ItemModel.__name__],
        nickname      = 'get',
        parameters    = [
            {
              "name": "_creator_id",
              "description": "Item creator id",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "query"
            },
            {
              "name": "media_id",
              "description": "Item media id",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "query"
            },
            {
              "name": "category_id",
              "description": "Item category id",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "query"
            },
            {
              "name": "EAN",
              "description": "Item EAN",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "query"
            },
            {
              "name": "ASIN",
              "description": "Item ASIN",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "query"
            },
            {
              "name": "ASIN_LINK_AMAZON",
              "description": "A link to Amazon regarding this item",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "name",
              "description": "Item name",
              "required": False,
              "allowMultiple": False,
              "dataType": "string ",
              "paramType": "query"
            },
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Item(s) found"
            },
            {
              "code": 404,
              "message": "Item(s) not found"
            }
        ]
    )    
    @use_args(args_optional)       
    def get(self, args):  
        if 'text' in args:
            print('find_text')
            items = ItemModel.find_text(**args)
        else:     
            items = ItemModel.find(**args)

        if items:
            itemsJSON = []
            for item in items:
                itemsJSON.append(item.json())
            return { "items" : itemsJSON}, 200 # OK
        else:
            return{"message":"Item not found"}, 404 #not found

    # POST      
    @swagger.operation(
        notes='Post an items list',
        responseClass = [ItemModel.__name__],
        nickname      = 'post',
        parameters    = [
            {
              "name": "_creator_id",
              "description": "Item creator id",
              "required": True,
              "allowMultiple": True,
              "dataType": "integer",
              "paramType": "form"
            },
            {
              "name": "media_id",
              "description": "Item media id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "form"
            },
            {
              "name": "category_id",
              "description": "Item category id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "form"
            },
            {
              "name": "EAN",
              "description": "Item EAN",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "form"
            },
            {
              "name": "ASIN",
              "description": "Item ASIN",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "form"
            },
            {
              "name": "ASIN_LINK_AMAZON",
              "description": "A link to Amazon regarding this item",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "form"
            },
            {
              "name": "name",
              "description": "Item name",
              "required": True,
              "allowMultiple": False,
              "dataType": "string ",
              "paramType": "form"
            },
        ],
        responseMessages = [
            {
              "code": 201,
              "message": "Item inserted"
            },
            {
              "code": 400,
              "message": "Item already exists"
            }
        ]
    )           
    @use_args(args_required)         
    def post(self, args):
      if ItemModel.find(strict=True, **args):
        return {"message":"An item named {} already exists".format(args['name'])}, 400
      item = ItemModel(**args)   
      # media = MediaModel(data['name'])
      # for each of the keys in data say key = value  
      # ie name = value
      item.save_to_db()    
      return{"message":"item {} created successfully".format(args['name'])}, 201 # created 