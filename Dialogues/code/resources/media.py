from flask_restful import Resource
from flask_restful_swagger import swagger

from webargs import fields
from webargs.flaskparser import use_args
from models.media import MediaModel

class Media(Resource):
    "Media resource"
    args_required = {
            'category' : fields.String(required=True,
                                       error_messages = {"required":"Media category cannot be blank"}),
    }
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
            return {'message': "media {} has been deleted".format(_id)},200        

        return {'message': "No media {} to delete".format(_id)},200        

    # PUT
    @swagger.operation(
        notes='Update a media, id is required',
        responseClass = [MediaModel.__name__],
        nickname      = 'put',
        parameters    = [
            {
              "name": "_id",
              "description": "Media id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            },
            {
              "name": "category",
              "description": "Media category",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            },
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Media updated"
            },
            {
              "code": 400,
              "message": "Media to update not found"
            }
        ]
    )              
    @use_args(args_required)         
    def put(self, args, _id):
        if MediaModel.find_by_category(args['category']):            
            return{"message":"Media category {} already exists".format(args['category'])}, 400 # category exists
        
        media = MediaModel.find_by_id(_id)
        if media:    
            media.category = args['category']                   
            media.save_to_db()    
            return {"message":"Media category {} has been updated".format(_id)}, 200
            
        return{"message":"Media id {} doesn't exists".format(_id)}, 400 # media to update not found        
    
class MediaList(Resource):    
    "MediaList resource"

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
            return{"message":"Media not found"}, 404 #not found

    # POST
    @swagger.operation(
        notes='Insert a media, category is required',
        responseClass = [MediaModel.__name__],
        nickname      = 'post',
        parameters    = [
            {
              "name": "category",
              "description": "Media category",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            },
        ],
        responseMessages = [
            {
              "code": 201,
              "message": "Media inserted"
            },
            {
              "code": 400,
              "message": "Media already exists"
            }
        ]
    )              
    @use_args(args_required)         
    def post(self, args):
        if MediaModel.find_by_category(args['category']):
            return {"message":"this media {} already exists".format(args['category'])}, 400

        media = MediaModel(**args)   
        # media = MediaModel(data['name'])
        # for each of the keys in data say key = value  
        # ie name = value
        media.save_to_db()    
        return{"message":"media {} created successfully".format(args['category'])}, 201 # created