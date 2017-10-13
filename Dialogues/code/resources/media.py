from flask_restful import Resource
from flask_restful_swagger import swagger

from webargs import fields
from webargs.flaskparser import use_args
from models.media import MediaModel

class Media(Resource):
    "Media resource"
    # GET
    @swagger.operation(
        notes='Get a media item by ID',
        responseClass = MediaModel.__name__,
        nickname      = 'get',
        parameters    = [
            {
              "name": "_id",
              "description": "Media id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            }
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Media found"
            },
            {
              "code": 404,
              "message": "Media not found"
            }
        ]
    )
    def get(self, _id):
        media = MediaModel.find_by_id(_id)
        if media:
            return media.json(), 200
        else:
            return{"message":"Media not found"}, 404

    # DELETE        
    @swagger.operation(
        notes='Delete a media item by id',
        responseClass = MediaModel.__name__,
        nickname      = 'delete',
        parameters    = [
            {
              "name": "_id",
              "description": "Media id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            }
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Media deleted"
            },
            {
              "code": 404,
              "message": "Media to delete not found"
            }
        ]
    )        
    def delete(self, _id):
        media = MediaModel.find_by_id(_id)
        
        if media:
            media.delete_from_db()
            return {'message': "media {} has been deleted".format(media.category)},200        

        return {'message': "No media {} to delete".format(media.category)},200        
    
class MediaList(Resource):    
    args_required = {
            'category' : fields.String(required=True,
                                   error_messages = {"required":"Media category cannot be blank"}),
    }
    
    args_optional = {
        'category' : fields.String(required=False),
    }    
    # GET      
    @swagger.operation(
        notes='Get a media list you may use category as filter',
        responseClass = [MediaModel.__name__],
        nickname      = 'get',
        parameters    = [
            {
              "name": "category",
              "description": "Media category",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Media(s) found"
            },
            {
              "code": 404,
              "message": "Media(s) not found"
            }
        ]
    )
    @use_args(args_optional)             
    def get(self,args):       
        medias = MediaModel.find(**args)   
        if medias:
            mediasJSON = []
            for media in medias:
                mediasJSON.append(media.json())
            return {"medias":mediasJSON}, 200 # OK
        else:
            return{"message":"Media {} not found".format(args['category'])}, 404 #not found

    # POST
    @swagger.operation(
        notes='Insert a media, category is required',
        responseClass = [MediaModel.__name__],
        nickname      = 'post',
        parameters    = [
            {
              "name": "category",
              "description": "Category lastname",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "body"
            },
        ],
        responseMessages = [
            {
              "code": 201,
              "message": "Category inserted"
            },
            {
              "code": 400,
              "message": "Category already exists"
            }
        ]
    )              
    @use_args(args_required)         
    def post(self,args):
        if MediaModel.find_by_category(args['category']):
            return {"message":"A media {} already exists".format(args['category'])}, 400

        media = MediaModel(**args)   
        # media = MediaModel(data['name'])
        # for each of the keys in data say key = value  
        # ie name = value
        media.save_to_db()    
        return{"message":"media {} created successfully".format(args['category'])}, 201 # created