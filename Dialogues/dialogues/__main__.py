from . import app

# __main__ is the special name assign by python for the file we run
# allow us to not execute app.run if app.py is imported into another program
def main():
   from db import db,whooshee
   with app.app_context():
       db.init_app(app)        
       whooshee.init_app(app)
       whooshee.reindex()

   app.run(port=5000, debug = True)

if __name__ == "__main__":
    main()