from flask_restful import Resource
from flask_restful_swagger import swagger

from webargs import fields
from webargs.flaskparser import use_args
from models.user import UserModel

class User(Resource):
    "User resource"
    args_required = {
            'name'     : fields.String(required=True,
                                       error_messages = {"required":"User name cannot be blank"}),
            'password' : fields.String(required=True,
                                       error_messages = {"required":"User password cannot be blank"}),
    }

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    # GET
    @swagger.operation(
        notes='Get a user item by ID',
        responseClass = UserModel.__name__,
        nickname      = 'get',
        parameters    = [
            {
              "name": "_id",
              "description": "User id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            }
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "User found"
            },
            {
              "code": 404,
              "message": "User not found"
            }
        ]
    )    
    def get(self, _id):
        user = UserModel.find_by_id(_id)
        if user:
            return user.json(), 200
        else:
            return{"message":"User id not found"}, 404

    # DELETE        
    @swagger.operation(
        notes='Delete a user item by id',
        responseClass = UserModel.__name__,
        nickname      = 'delete',
        parameters    = [
            {
              "name": "_id",
              "description": "User id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            }
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "User deleted"
            },
            {
              "code": 404,
              "message": "User to delete not found"
            }
        ]
    )     
    def delete(self, _id):
        user = UserModel.find_by_id(_id)
        if user:
            user.delete_from_db()
        return {'message': "user id {} has been deleted".format(user.id)},200        

    # PUT
    @swagger.operation(
        notes='Update a user, id is required',
        responseClass = [UserModel.__name__],
        nickname      = 'put',
        parameters    = [
            {
              "name": "_id",
              "description": "User id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            },
            {
              "name": "name",
              "description": "User name",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            },
            {
              "name": "password",
              "description": "User password",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            },
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "User updated"
            },
            {
              "code": 400,
              "message": "User to update not found"
            }
        ]
    )              
    @use_args(args_required)         
    def put(self, args, _id):
        user = UserModel.find_by_id(_id)
        if user:    
            user.name = args['name']                   
            user.password = args['password']                   
            user.save_to_db()    
            return {"message":"User id {} has been updated".format(_id)}, 200
            
        return{"message":"User id {} doesn't exists".format(_id)}, 400 # media to update not found        
    
class UserList(Resource):    
    "UserList resource"    
    args = {
            'username' : fields.String(required=True,
                                       error_messages = {"required":"Username cannot be blank"}),
    }

    # GET      
    @swagger.operation(
        notes='Get a user list, name may be use as filter',
        responseClass = [UserModel.__name__],
        nickname      = 'get',
        parameters    = [
            {
              "name": "username",
              "description": "User name",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "User(s) found"
            },
            {
              "code": 404,
              "message": "User(s) not found"
            }
        ]
    )    
    @use_args(args)
    def get(self,args):       
        user = UserModel.find_by_username(**args)
        if user:
            return user.json(), 200 # OK
        else:
            return{"message":"Username {} not found".format(args['username'])}, 404 #not found

class UserRegister(Resource):
    "UserRegister resource"
    
    args = {
            'username' : fields.String(required=True,
                                       error_messages = {
                                        "required":"Username cannot be blank"
                                       }),
            'password' : fields.String(required=True,
                                       error_messages = {
                                           "required":"password cannot be blank"
                                       }),
    } 

    # POST
    @swagger.operation(
        notes='Insert a user, name and password are required',
        responseClass = [UserModel.__name__],
        nickname      = 'post',
        parameters    = [
            {
              "name": "username",
              "description": "User name",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            },
            {
              "name": "password",
              "description": "User password",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "form"
            },
        ],
        responseMessages = [
            {
              "code": 201,
              "message": "User inserted"
            },
            {
              "code": 400,
              "message": "User already exists"
            }
        ]
    )      
    @use_args(args)     
    def post(self,args):
        if (UserModel.find_by_username(args['username'])):
            return {"message":"A User with this username already exists"}, 400

        user = UserModel(**args)   
        # user = UserModel(data['username'], data['password'])
        # for each of the keys in data say key = value  
        # ie username = value, password = value
        user.save_to_db()

        return{"message":"User created successfully"}, 201 