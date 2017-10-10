from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from models.item import ItemModel


class Item(Resource):
    def get(self, _id):
        item = ItemModel.find_by_id(_id)
        if item:
            return item.json(), 200
        else:
            return{"message":"Item id not found"}, 404

    def delete(self, _id):
        item = ItemModel.find_by_id(_id)
        
        if item:
            item.delete_from_db()
            return {'message': "item id {} has been deleted".format(item.id)},200        

        return {'message': "No item id {} to delete".format(item.category)},200        
    
class ItemList(Resource):    
    args_required = {
            'creator_id'    : fields.Integer(required=True,
                                             error_messages = {"required":"Creator id cannot be blank"}),
            'media_id'      : fields.Integer(required=True,
                                             error_messages = {"required":"Media id cannot be blank"}),
            'category_id'   : fields.Integer(required=True,
                                             error_messages = {"required":"Category id cannot be blank"}),
            'EAN'           : fields.Integer(),
            'ASIN'          : fields.Integer(),
            'name'          : fields.String(required=True,
                                            error_messages = {"required":"Name cannot be blank"}),
            'synopsys'      : fields.String(),
            'creation_date' : fields.DateTime(),
    }

    args_optional = {
            'creator_id'    : fields.Integer(required=False),
            'media_id'      : fields.Integer(required=False),
            'category_id'   : fields.Integer(required=False),
            'EAN'           : fields.Integer(),
            'ASIN'          : fields.Integer(),
            'name'          : fields.String(),
            'synopsys'      : fields.String(),
            'creation_date' : fields.DateTime(),
            'text'          : fields.String(), 
    }
        
    @use_args(args_optional)       
    def get(self, args):  
        print(args)
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

    @use_args(args_required)         
    def post(self, args):
        
        if ItemModel.find(strict=True, **args):
            return {"message":"An item named {} already exists".format(args['name'])}, 400

        item = ItemModel(**args)   
        # media = MediaModel(data['name'])
        # for each of the keys in data say key = value  
        # ie name = value
        item.save_to_db()    
        return{"message":"item {} created successfully".format(args['name'])}, 201 # crea

    @use_args(args_required)         
    def delete(self, args):
        item = ItemModel.find(**args)

        if item:
            item.delete_from_db()
            return {'message': "item {} has been deleted".format(args['name'])},200    

        return {'message': "No item {} to delete".format(args['namecreator_id'])},200            