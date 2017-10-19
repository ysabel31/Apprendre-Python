from flask_restful import Resource
from flask_restful_swagger import swagger

from webargs import fields
from webargs.flaskparser import use_args
from models.creator import CreatorModel


class Creator(Resource):
    "Creator resource"

    args_required = {
         'lastname'  : fields.String(required = True,
                                     error_messages = { "required": "Creator lastname cannot be blank"}),
         'firstname' : fields.String(required = False),
    }   

    # GET
    @swagger.operation(
        notes='Get a creator item by ID',
        responseClass = CreatorModel.__name__,
        nickname      = 'get',
        parameters    = [
            {
              "name": "_id",
              "description": "Creator id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            }
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Creator found"
            },
            {
              "code": 404,
              "message": "Creator not found"
            }
        ]
    )
    def get(self, _id):        
        creator = CreatorModel.find_by_id(_id)
    
        if creator:
            return creator.json(), 200 # OK
        else:
            return{"message":"Creator {} not found".format(_id)}, 404 #not found

    # DELETE        
    @swagger.operation(
        notes='Delete a creator item by id',
        responseClass = CreatorModel.__name__,
        nickname      = 'delete',
        parameters    = [
            {
              "name": "_id",
              "description": "Creator id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            }
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Creator deleted"
            },
            {
              "code": 404,
              "message": "Creator to delete not found"
            }
        ]
    )        
    def delete(self, _id):
        creator = CreatorModel.find_by_id(_id)
        if creator:
            creator.delete_from_db()
            return {'message': "Creator id {} has been deleted".format(_id)},200
        return {'message': "No Creator id {} to delete".format(_id)},404

    # PUT
    @swagger.operation(
        notes='Update a creator, id is required',
        responseClass = [CreatorModel.__name__],
        nickname      = 'put',
        parameters    = [
            {
              "name": "_id",
              "description": "Creator id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            },
            {
              "name": "firstname",
              "description": "Creator firstname",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            },            
            {
              "name": "lastname",
              "description": "Creator lastname",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
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
    def put(self, args, _id):
        print(args)
        creator = CreatorModel.find_by_id(_id)
        if creator:    
            creator.name = args['firstname']                   
            creator.name = args['lastname']                   
            creator.save_to_db()    
            return {"message":"Creator {} has been updated".format(_id)}, 200
            
        return{"message":"Creator id {} doesn't exists".format(_id)}, 400 # media to update not found         

class CreatorList(Resource):    
    "Creator List resource"

    args_required = {
         'lastname'  : fields.String(required = True,
                                     error_messages = { "required": "Creator lastname cannot be blank"}),
         'firstname' : fields.String(required = False),
    }       

    args_optional = {
         'lastname'   : fields.String(required = False),
         'firstname'  : fields.String(required = False),         
    }

    # Error messages
    def ErrMsg(self,msg,args):
        if 'lastname' in args.keys() & 'firstname' in args.keys():
            return {"message":"Creator called {} {} {}".format(args['lastname'],args['firstname'],msg)}
        elif 'lastname' in args.keys():                    
            return {"message":"Creator lastname {} {} ".format(args['lastname'],msg)}
        elif 'firstname' in args.keys():                    
            return {"message":"Creator firstname {} {} ".format(args['firstname'],msg)}

    
    # GET      
    @swagger.operation(
        notes='Get a creator list using lastname and/or firstname as filters',
        responseClass = [CreatorModel.__name__],
        nickname      = 'get',
        parameters    = [
            {
              "name": "lastname",
              "description": "Creator lastname",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            },
            {
              "name": "firstname",
              "description": "Creator firstname",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            }
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Creator(s) found"
            },
            {
              "code": 404,
              "message": "Creator(s) not found"
            }
        ]
    )
    @use_args(args_optional)  
    def get(self,args):       
        creators = CreatorModel.find(**args)        
        if creators:
            creatorsJSON = []
            for creator in creators:
                creatorsJSON.append(creator.json())
            return {"creators":creatorsJSON}, 200 # OK
        else:
            return self.ErrMsg("not found",args), 404 # Not found

    # POST
    @swagger.operation(
        notes='Insert a creator, lastname is required',
        responseClass = [CreatorModel.__name__],
        nickname      = 'post',
        parameters    = [
            {
              "name": "lastname",
              "description": "Creator lastname",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            },
            {
              "name": "firstname",
              "description": "Creator firstname",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            }
        ],
        responseMessages = [
            {
              "code": 201,
              "message": "Creator inserted"
            },
            {
              "code": 400,
              "message": "Creator already exists"
            }
        ]
    )         
    @use_args(args_required)        
    def post(self, args):
        creator = CreatorModel(**args)   
        # creator = CreatorModel(data['username'], data['password'])
        # for each of the keys in data say key = value  
        # ie username = value, password = value
        creator.save_to_db()

        return self.ErrMsg("created successfully",args), 201 # created

    