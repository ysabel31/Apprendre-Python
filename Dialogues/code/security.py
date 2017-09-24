from models.user import UserModel
from werkzeug.security import safe_str_cmp 
 
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    # safer way to compare string
    if user and safe_str_cmp(user.password, password):
    # With python 2.7 it's not a good idea to compare string with directly == 
    # = en python 3.6 if user and user.password == password:
        return user

def identity(payload):
    # payload = contents of JWT token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
