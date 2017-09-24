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
        data = Creator.parser.parse_args()  
        if CreatorModel.find_by_name(**data):
            return {"message":"A creator with this identity already exists"}, 400

        creator = CreatorModel(**data)   
        # user = UserModel(data['username'], data['password'])
        # for each of the keys in data say key = value  
        # ie username = value, password = value
        creator.save_to_db()

        return{"message":"Creator created successfully"}, 201

    def get(self, firstname, lastname):
        data = Creator.parser.parse_args()  
        creator = CreatorModel.find_by_name(**data)
        if creator:
            return creator.json(), 200
        else:
            return{"message":"Creator not found"}, 404