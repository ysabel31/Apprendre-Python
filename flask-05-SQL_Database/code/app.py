from flask import Flask,request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

#jsonify is a method not a class
app = Flask(__name__)
app.secret_key= 'asdf'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth
items =[]
# define resource Student
class Item(Resource):
    # define methods that this ressource accepts
    # item is going to be a dictionarya dictionary
    # no longer need to do jsonify beacuse when using Flask RESTful does it for us    

    # To make sure that price is passed in
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help = "This field cannot be left blank !")

    @jwt_required()
    def get(self, name):
        #for item in items:
        #    if item['name'] == name:
        #        return item
        # filter usage next give us the first item encountered, 
        # Generate an error if no item found, with None it will return a None
        item = next(filter(lambda x : x['name'] == name, items) , None )
        return {'item':item}, 200 if item else 404
                    
    def post(self, name):
        data = Item.parser.parse_args()
        
        if next(filter(lambda x : x['name'] == name, items), None):
             return {'message': "An item with name'{}'already exists.".format(name)} 

        # get_json(force=True)
        # You don't need content type Header, 
        # it will just look in the content and it will format 
        # even if the content type header is not set application/json
        # dangerous 
        # get_json(silent=True)
        # it doesn't give an error just return none    

        #data = request.get_json()
        item = {'name' : name, 'price':data['price']}    
        items.append(item)
        return item, 201

    def delete(self,name):
        # Variable items = global variable not local 
        global items
        # local variable named items, it will use variable before define it  
        # don't work usage of global variable 
        items = list(filter(lambda x : x['name'] != name, items ))    
        return {'message':'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x : x['name'] == name, items), None)
        # if not found create item
        if item is None:
            item = {'name': name ,'price' : data['price']} 
            items.append(item)
        else:        
            item.update(data)
        return item

class ItemList(Resource):
    # Define methods that this ressource accepts     
    def get(self):
        return {'items': items}
                    
    def post(self, name):
        item = {'name' : name, 'price':12.00}    
        items.append(item)
        return item, 201


api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList, '/items') 
app.run(port=5000, debug = True)