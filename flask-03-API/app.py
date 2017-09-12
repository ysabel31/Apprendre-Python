from flask import Flask, jsonify, request, render_template
#jsonify is a method not a class
app = Flask(__name__)
# dictionnary for this exercice  
# NB JSON is dictionary useful to share data between applications ;-)
stores = [
            {
                'name':'My Wonderful Store',
                'items':[
                        {
                            'name':'My item',
                            'price': 15.99
                        }

                ]
            }
        ]   

# POST - used to receive data
# GET - used to send data back only
# in our case we are server not browser it's the opposite point of view 

# POST /store data : {name:} 
#   Create a new store with a given name

#@app.route('/') # by example 'http://google.com/' = google's inpoint 
# by Default is methods = GET
@app.route('/store', methods = ['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name' : request_data['name'],
        'items' : []        
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name> => 
# Get a store for a given name and return some data about it
@app.route('/store/<string:name>') # 'http://127.0.0.1:5000/store/some_name' some_name = name
def get_store(name):
    # Iterate over stores
    # if the store matches, return it
    # if none match, return an error message
    for store in stores:
        if store['name'] == name:
            return jsonify(store)

    return jsonify({'message':'Store not found'})


# GET /store 
# Return a list of stores
@app.route('/store')
def get_stores():
    # create a dictionary that contains a list of stores because of JSON must be a dictionary
    return jsonify({'stores':stores})


# POST /store/<string:name>/item {name:, price:}
#   Create an item 
@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)        
    
    return jsonify({'message':'store not found'})
    

# GET /store/<string:name>/item  
#   Get all the items in a specific store
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})

        return jsonify({'message':'store not found'})
# tell app exactly what request it will understand
@app.route('/')
def home():
    return render_template('index.html')

app.run(port=5000)