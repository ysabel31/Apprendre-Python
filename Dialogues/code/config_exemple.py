SQLALCHEMY_DATABASE_URI = 'mysql://root:mdp@adr.mydb.fr/dbname'
# turn off the Flask SQLAlchemy modification tracker 
# it does not turn off the SQLAlchemy modification tracker 
SQLALCHEMY_TRACK_MODIFICATIONS = False 

# set the location for the whoosh index
WHOOSHEE_DIR = '../whoosh_index'

SECRET_KEY = 'secret_key'