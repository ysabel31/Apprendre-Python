from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from models.user import UserModel

class User(Resource):
    def get(self, _id):
        user = UserModel.find_by_id(_id)
        if user:
            return user.json(), 200
        else:
            return{"message":"User id not found"}, 404

    def delete(self, _id):
        user = UserModel.find_by_id(_id)
        if user:
            user.delete_from_db()
        return {'message': "user id {} has been deleted".format(user.id)},200        
    
class UserList(Resource):    
    args = {
            'username' : fields.String(required=True,
                                       error_messages = {"required":"Username cannot be blank"}),
    }
        
    @use_args(args)
    def get(self,args):       
        user = UserModel.find_by_username(**args)
        if user:
            return user.json(), 200 # OK
        else:
            return{"message":"Username {} not found".format(args['username'])}, 404 #not found

    @use_args(args)         
    def delete(self, args):
        user = UserModel.find_by_username(args['username'])
        if user:
            user.delete_from_db()
        return {'message': "Username {} has been deleted".format(user.username)},200      

class UserRegister(Resource):
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