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

    args = {'firstname' : fields.String,
            'lastname' : fields.String}        
    
    def get(self):       
        creator = CreatorModel.find_by_name(**data)
        if creator:
            print("json")
            return creator.json(), 200 # OK
        else:
            return{"message":"Creator not found"}, 404 #not found

    @use_args(args)        
    def post(self):
        if CreatorModel.find_by_name(**data):
            return {"message":"A creator named {} {} already exists".format(data['lastname'],data['firstname'])}, 400 # Bad request

        creator = CreatorModel(**data)   
        # creator = CreatorModel(data['username'], data['password'])
        # for each of the keys in data say key = value  
        # ie username = value, password = value
        creator.save_to_db()

        return{"message":"Creator created successfully"}, 201 # created