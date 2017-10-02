from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from models.item import ItemModel

class Item(Resource):
    def get(self, _id):
        media = MediaModel.find_by_id(_id)
        if media:
            return media.json(), 200
        else:
            return{"message":"Media category not found"}, 404

    def delete(self, _id):
        media = MediaModel.find_by_id(_id)
        
        if media:
            media.delete_from_db()
            return {'message': "media category {} has been deleted".format(media.category)},200        

        return {'message': "No media category {} to delete".format(media.category)},200        
    
class ItemList(Resource):    
    args = {
            creator_id = fields.Integer(required=True,
                                        error_messages = {"required":"Creator id cannot be blank"}),
            media_id = fields.Integer(required=True,
                                        error_messages = {"required":"Media id cannot be blank"}),
            category_id = fields.Integer(required=True,
                                        error_messages = {"required":"Category id cannot be blank"}),
            EAN = fields.Integer(),
            ASIN = fields.Integer(),
            name = fields.String(),
            synopsys = fields.String(),
            creation_date= fields.DateTime()),
    }
        
    @use_args(args)       
    def get(self,args):       
        media = MediaModel.find_by_category(**args)
        if media:
            return media.json(), 200 # OK
        else:
            return{"message":"Media category {} not found".format(args['category'])}, 404 #not found

    @use_args(args)         
    def post(self,args):
        if MediaModel.find_by_category(args['category']):
            return {"message":"A media category {} already exists".format(args['category'])}, 400

        media = MediaModel(**args)   
        # media = MediaModel(data['name'])
        # for each of the keys in data say key = value  
        # ie name = value
        media.save_to_db()    
        return{"message":"media {} created successfully".format(args['category'])}, 201 # crea

    @use_args(args)         
    def delete(self, args):
        media = MediaModel.find_by_category(args['category'])

        if media:
            media.delete_from_db()
            return {'message': "media category {} has been deleted".format(args['category'])},200    

        return {'message': "No media category {} to delete".format(args['category'])},200            