from werkzeug.security import safe_str_cmp 
from user import User 
users = [
    User(1, 'bob', 'gqfdgqf')    
]

username_mapping = { u.username : u for u in users }

userid_mapping = { u.id : u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    #safer way to compare string
    if user and safe_str_cmp(user.password,password):
    # with python 2.7 it's not a good idea to compare string with directly == 
    # = if user and user.password == password:
        return user

def identity(payload):
    #payload = contents of JWT token
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
