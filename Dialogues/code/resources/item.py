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
    args = {
            'creator_id'    : fields.Integer(required=True,
                                             error_messages = {"required":"Creator id cannot be blank"}),
            'media_id'      : fields.Integer(required=True,
                                             error_messages = {"required":"Media id cannot be blank"}),
            'category_id'   : fields.Integer(required=True,
                                             error_messages = {"required":"Category id cannot be blank"}),
            'EAN'           : fields.Integer(),
            'ASIN'          : fields.Integer(),
            'name'          : fields.String(),
            'synopsys'      : fields.String(),
            'creation_date' : fields.DateTime(),
    }
        
    @use_args(args)       
    def get(self,args):       
        item = ItemModel.find_by_category(**args)
        if item:
            return item.json(), 200 # OK
        else:
            return{"message":"Item category {} not found".format(args['category'])}, 404 #not found

    @use_args(args)         
    def post(self,args):
        if ItemModel.find_by_name(args['name']):
            return {"message":"An item named {} already exists".format(args['name'])}, 400

        item = ItemModel(**args)   
        # media = MediaModel(data['name'])
        # for each of the keys in data say key = value  
        # ie name = value
        item.save_to_db()    
        return{"message":"item {} created successfully".format(args['name'])}, 201 # crea

    @use_args(args)         
    def delete(self, args):
        item = ItemModel.find_by_name(args['name'])

        if item:
            item.delete_from_db()
            return {'message': "item {} has been deleted".format(args['name'])},200    

        return {'message': "No item {} to delete".format(args['namecreator_id'])},200            