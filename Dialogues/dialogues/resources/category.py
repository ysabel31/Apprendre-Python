from flask_restful import Resource
from flask_restful_swagger import swagger

from webargs import fields
from webargs.flaskparser import use_args

from models.category import CategoryModel


class Category(Resource):
    "Category resource"

    args_required = {
        'name' : fields.String(required = True,
                               error_messages = { "required": "Category name cannot be blank"}),
    } 

    # GET
    @swagger.operation(
        notes         ='Get a category item by ID',
        responseClass = CategoryModel.__name__,
        nickname      = 'get',
        parameters    = [
            {
                "name"          : "_id",
                "description"   : "Category id",
                "required"      : True,
                "allowMultiple" : False,
                "dataType"      : "integer",
                "paramType"     : "path"
            }
        ],
        responseMessages = [
            {
              "code"    : 200,
              "message" : "Category found"
            },
            {
              "code"    : 404,
              "message" : "Category not found"
            }
        ]
    )
    def get(self, _id):
        category = CategoryModel.find_by_id(_id)
    
        if category:
            return category.json(), 200 # OK
        else:
            return{"message":"Category {} not found".format(_id)}, 404 #not found
    
    # DELETE        
    @swagger.operation(
        notes         = 'Delete a category item by id',
        responseClass = CategoryModel.__name__,
        nickname      = 'delete',
        parameters    = [
            {
              "name"          : "_id",
              "description"   : "Category id",
              "required"      : True,
              "allowMultiple" : False,
              "dataType"      : "integer",
              "paramType"     : "path"
            }
        ],
        responseMessages = [
            {
              "code"    : 200,
              "message" : "Category deleted"
            },
            {
              "code"    : 404,
              "message" : "Category to delete not found"
            }
        ]
    )      
    def delete(self, _id):
        category = CategoryModel.find_by_id(_id)
        if category:
            category.delete_from_db()
            return {'message': "Category id {} has been deleted".format(_id)},200
        return {'message': "No Category id {} to delete".format(_id)},404

    # PUT
    @swagger.operation(
        notes         = 'Update a category, id is required',
        responseClass = [CategoryModel.__name__],
        nickname      = 'put',
        parameters    = [
            {
              "name"          : "_id",
              "description"   : "Category id",
              "required"      : True,
              "allowMultiple" : False,
              "dataType"      : "integer",
              "paramType"     : "path"
            },
            {
              "name"          : "name",
              "description"   : "Category name",
              "required"      : True,
              "allowMultiple" : False,
              "dataType"      : "string",
              "paramType"     : "form"
            },
        ],
        responseMessages = [
            {
              "code"    : 200,
              "message" : "Category updated"
            },
            {
              "code"    : 400,
              "message" : "Category to update not found"
            }
        ]
    )              
    @use_args(args_required)         
    def put(self, args, _id):
        if CategoryModel.find_by_name(args['name']):            
            return{"message" : "Category name {} already exists".format(args['name'])}, 400 # category exists
        
        category = CategoryModel.find_by_id(_id)
        if category:    
            category.name = args['name']                   
            category.save_to_db()    
            return {"message" : "Category name {} has been updated".format(_id)}, 200
            
        return{"message" : "Category id {} doesn't exists".format(_id)}, 400 # media to update not found     


class CategoryList(Resource):    
    "CategoryList resource"
          
    args_required = {
        'name'  : fields.String(required = True,
                                error_messages = { "required" : "Category name cannot be blank"}),
    }       

    args_optional = {
        'name'  : fields.String(required = False),
    }

    # GET      
    @swagger.operation(
        notes         = 'Get a category list, name may be use as filter',
        responseClass = [CategoryModel.__name__],
        nickname      = 'get',
        parameters    = [
            {
              "name"          : "name",
              "description"   : "Category name",
              "required"      : False,
              "allowMultiple" : False,
              "dataType"      : "string",
              "paramType"     : "query"
            },
        ],
        responseMessages = [
            {
              "code"    : 200,
              "message" : "Category(ies) found"
            },
            {
              "code"    : 404,
              "message" : "Category(ies) not found"
            }
        ]
    )
    @use_args(args_optional)       
    def get(self,args):       
        categories = CategoryModel.find(**args)        

        if categories:
            categoriesJSON = []
            for category in categories:
                categoriesJSON.append(category.json())
            return {"categories" : categoriesJSON},200 #OK    
        else:
            return{"message" : "Category not found "}, 404 #not found
    
    # POST
    @swagger.operation(
        notes         = 'Insert a category, name is required',
        responseClass = [CategoryModel.__name__],
        nickname      = 'post',
        parameters    = [
            {
              "name"          : "name",
              "description"   : "Category name",
              "required"      : True,
              "allowMultiple" : False,
              "dataType"      : "string",
              "paramType"     : "form"
            },
        ],
        responseMessages = [
            {
              "code"    : 201,
              "message" : "Category inserted"
            },
            {
              "code"    : 400,
              "message" : "Category already exists"
            }
        ]
    )      
    @use_args(args_required)       
    def post(self,args):        
        if CategoryModel.find_by_name(**args):
            return {"message" : "A category named {} already exists".format(args['name'])}, 400 # Bad request

        category = CategoryModel(**args)   
        # creator = CreatorModel(data['username'], data['password'])
        # for each of the keys in data say key = value  
        # ie username = value, password = value
        category.save_to_db()

        return{"message" : "Category {} created successfully".format(args['name'])}, 201 # created