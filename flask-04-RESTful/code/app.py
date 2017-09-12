from flask import Flask
from flask_restful import Resource, Api

#jsonify is a method not a class
app = Flask(__name__)
api = Api(app)

# define resource Student
class Student(Resource):
    # define methods that this ressource accepts
    def get(self, name):
        return {'student': name}

api.add_resource(Student, '/student/<string:name>') # http://127.0.0.1:5000/student/Rolf

app.run(port=5000)