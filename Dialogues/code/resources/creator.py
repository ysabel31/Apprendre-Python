from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from models.creator import CreatorModel

class Creator(Resource):
    def get(self, _id):
        creator = CreatorModel.find_by_id(_id)
    
        if creator:
            return creator.json(), 200 # OK
        else:
            return{"message":"Creator not found"}, 404 #not found

    def delete(self, firstname, lastname):
        creator = CreatorModel.find_by_name(firstname, lastname)
        if creator:
            creator.delete_from_db()
        return {'message': "Creator named {} {} has been deleted".format(lastname,firstname)},200

class CreatorList(Resource):    

    args = {
         'lastname'  : fields.String(required = True,
                                     error_messages = { "required": "Creator lastname cannot be blank"}),
         'firstname' : fields.String(required = True, 
                                     error_messages = {"required":"Creator firstname cannot be blank"}),
    }       

    @use_args(args)       
    def get(self,args):       
        creator = CreatorModel.find_by_name(**args)
        if creator:
            return creator.json(), 200 # OK
        else:
            return{"message":"Creator not found"}, 404 #not found

    @use_args(args)        
    def post(self, args):
        
        if CreatorModel.find_by_name(**args):
            return {"message":"A creator named {} {} already exists".format(args['lastname'],args['firstname'])}, 400 # Bad request

        creator = CreatorModel(**args)   
        # creator = CreatorModel(data['username'], data['password'])
        # for each of the keys in data say key = value  
        # ie username = value, password = value
        creator.save_to_db()

        return{"message":"Creator created successfully"}, 201 # created