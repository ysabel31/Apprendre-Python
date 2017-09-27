from flask_restful import Resource, reqparse
from models.media import MediaModel

class Media(Resource):
    
    parser = reqparse.RequestParser()

    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Media name cannot be blank ")

    def get(self, name):
        #input check
        data = Media.parser.parse_args()  
        # Search database 
        # **data = json from the request body converted into dict
        media = MediaModel.find_by_name(**data)
        if media:
            return media.json(), 200
        else:
            return{"message":"Media not found"}, 404

    def post(self):
        data = Media.parser.parse_args()  
        if MediaModel.find_by_name(**data):
            return {"message":"This media already exists"}, 400

        media = MediaModel(**data)   
        # media = MediaModel(data['name'])
        # for each of the keys in data say key = value  
        # ie name = value
        media.save_to_db()

    def delete(self):
        media = MediaModel.find_by_name(name)
        if media:
            media.delete_from_db()
        return {'message': 'Media deleted'},200                