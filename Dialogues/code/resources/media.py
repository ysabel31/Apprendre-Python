from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from models.media import MediaModel

class Media(Resource):
    args = {
         'name'  : fields.String(required=True,
                                 error_messages = {
                                                    "required":"Media name cannot be blank"
                                                  }),
    }

    @use_args(args) 
    def get(self, args):
        media = MediaModel.find_by_name(**args)
        if media:
            return media.json(), 200
        else:
            return{"message":"Media not found"}, 404

    @use_args(args)         
    def post(self,args):
        if MediaModel.find_by_name(**args):
            return {"message":"This media already exists"}, 400

        media = MediaModel(**args)   
        # media = MediaModel(data['name'])
        # for each of the keys in data say key = value  
        # ie name = value
        media.save_to_db()

    @use_args(args)  
    def delete(self,args):
        media = MediaModel.find_by_name(**args)
        if media:
            media.delete_from_db()
        return {'message': 'Media deleted'},200                