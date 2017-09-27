from flask_restful import Resource, reqparse
from models.creator import CreatorModel

class Creator(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('firstname', 
                        type=str,
                        required=True,
                        help="First name cannot be blank!")

    parser.add_argument('lastname', 
                        type=str,
                        required=True,
                        help="Last name cannot be blank!")
    
    def post(self):
        #input check
        data = Creator.parser.parse_args()  
        # Search database 
        # **data = json from the request body converted into dict
        if CreatorModel.find_by_name(**data):
            return {"message":"A creator named {} {} already exists".format(data['lastname']).format(data['firstname'])}, 400 # Bad request

        creator = CreatorModel(**data)   
        # creator = CreatorModel(data['username'], data['password'])
        # for each of the keys in data say key = value  
        # ie username = value, password = value
        creator.save_to_db()

        return{"message":"Creator created successfully"}, 201 # created

    def get(self, lastname, firstname):
        creator = CreatorModel.find_by_name(firstname, lastname)
        if creator:
            return creator.json(), 200 # OK
        else:
            return{"message":"Creator not found"}, 404 #not found

    def delete(self, firstname, lastname):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'},200