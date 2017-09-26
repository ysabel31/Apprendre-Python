import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

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

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items where name = ?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()

        if row:
            return {"item" : {'name' : row[0], 'price' : row[1]}}
        
        connection.close()
    
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items(name, price) VALUES(?, ?)"
        cursor.execute(query,(item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items set price = ? WHERE name = ?"
        cursor.execute(query,(item['price'], item['name']))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'item not found'}, 404    

    
    def post(self, name):
        if self.find_by_name(name):
             return {'message': "An item with name'{}'already exists.".format(name)} 

        data = Item.parser.parse_args()
        
        item = {'name' : name, 'price':data['price']}    
        try:
            self.insert(item)
        except:
            return{'message':'An error occur inserting the item'}, 500 # Internal server error 
        
        return item, 201

    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()
        return {'message':'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        
        item = self.find_by_name(name)
        updated_item = {'name': name ,'price' : data['price']} 

        # if not found create item
        if item is None:     
            try:       
                self.insert(updated_item)
            except:
                return{'message':"An error occured inserting the item."}, 500    
        else:        
            try:
                self.update(updated_item)
            except:
                return{'message':"An error occured updating the item."}, 500    

        return updated_item

class ItemList(Resource):
    # Define methods that this ressource accepts     
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append(
                         { 'name'  : row[0],
                           'price' : row[1]
                         }
                        )
        
        connection.close()
        
        return {'items': items}