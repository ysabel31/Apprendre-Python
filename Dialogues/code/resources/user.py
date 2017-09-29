from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from models.user import UserModel

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