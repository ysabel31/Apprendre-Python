from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# define resource Item
class Item(Resource):
    # Resources are built on top of Flask pluggable views, 
    # giving you easy access to multiple HTTP methods 
    # just by defining methods on your resource
    
    # In this case Item Resource is added in app.py with this line :
    # api.add_resource(Item, '/item/<string:name>')

    # below is defined methods that this ressource accepts
    # item is going to be a dictionary
    # no longer need to do jsonify because Flask RESTful does it for us    

    # To make sure that price is passed in
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                         type=float,
                         required=True,
                         help = "This field cannot be left blank !")

    parser.add_argument('store_id',
                         type=int,
                         required=True,
                         help = "Every Item need a store id !")
    

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404    

    
    def post(self, name):
        if ItemModel.find_by_name(name):
             return {'message': "An item with name'{}'already exists.".format(name)} 

        data = Item.parser.parse_args()
        
        #item = ItemModel(name, data['price', data['store_id'])    
        item = ItemModel(name, **data)    
        try:
            item.save_to_db()
        except:
            return{'message':'An error occur inserting the item'}, 500 # Internal server error 
        
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)

        # if not found create item
        if item is None:     
            #item = ItemModel(name , data['price'], data['store_id']) 
            item = ItemModel(name , **data) 
        else:        
            item.price = data['price'] 

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    # Define methods that this ressource accepts     
    def get(self):
        return {'items' : [ item.json() for item in ItemModel.query.all()]}
        # = return {'items' : list(map(lambda x : x.json(), ItemModel.query.all()))}
        