from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from models.category import CategoryModel

class Category(Resource):
    def get(self, _id):
        category = CategoryModel.find_by_id(_id)
    
        if category:
            return category.json(), 200 # OK
        else:
            return{"message":"Category {} not found".format(_id)}, 404 #not found

    def delete(self, _id):
        category = CategoryModel.find_by_id(_id)
        if category:
            category.delete_from_db()
            return {'message': "Category id {} has been deleted".format(_id)},200
        return {'message': "No Category id {} to delete".format(_id)},200

class CategoryList(Resource):    

    args_required = {
         'name'  : fields.String(required = True,
                                 error_messages = { "required": "Category name cannot be blank"}),
    }       

    args_optional = {
         'name'  : fields.String(required = False),
    }

    @use_args(args_optional)       
    def get(self,args):       
        categories = CategoryModel.find(**args)        

        if categories:
            categoriesJSON = []
            for category in categories:
                categoriesJSON.append(category.json())
            return {"categories":categoriesJSON},200 #OK    
        else:
            return{"message" : "Category named {} not found ".format(args['name'])}, 404 #not found

    @use_args(args_required)        
    def post(self, args):
        
        if CategoryModel.find_by_name(**args):
            return {"message":"A category named {} already exists".format(args['name'])}, 400 # Bad request

        category = CategoryModel(**args)   
        # creator = CreatorModel(data['username'], data['password'])
        # for each of the keys in data say key = value  
        # ie username = value, password = value
        category.save_to_db()

        return{"message":"Category {} created successfully".format(args['name'])}, 201 # created

    @use_args(args_required)         
    def delete(self,args):
        category = CategoryModel.find_by_name(**args)
        if category:
            category.delete_from_db()
            return {'message': "Category named {} has been deleted".format(args['name'])},200
        return {'message': "No Category named {} to delete".format(args['name'])},200