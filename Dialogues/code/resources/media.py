from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from models.media import MediaModel

class Media(Resource):
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
    
class MediaList(Resource):    
    args_required = {
            'category' : fields.String(required=True,
                                   error_messages = {"required":"Media category cannot be blank"}),
    }
    
    args_optional = {
        'category' : fields.String(required=False),
    }    

    @use_args(args_optional)             
    def get(self,args):       
        medias = MediaModel.find(**args)   
        if medias:
            mediasJSON = []
            for media in medias:
                mediasJSON.append(media.json())
            return {"medias":mediasJSON}, 200 # OK
        else:
            return{"message":"Media category {} not found".format(args['category'])}, 404 #not found

    @use_args(args_required)         
    def post(self,args):
        if MediaModel.find_by_category(args['category']):
            return {"message":"A media category {} already exists".format(args['category'])}, 400

        media = MediaModel(**args)   
        # media = MediaModel(data['name'])
        # for each of the keys in data say key = value  
        # ie name = value
        media.save_to_db()    
        return{"message":"media {} created successfully".format(args['category'])}, 201 # crea

    @use_args(args_required)         
    def delete(self, args):
        media = MediaModel.find_by_category(args['category'])

        if media:
            media.delete_from_db()
            return {'message': "media category {} has been deleted".format(args['category'])},200    

        return {'message': "No media category {} to delete".format(args['category'])},200            