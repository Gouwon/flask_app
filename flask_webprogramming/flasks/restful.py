from . import app
from flask import request
from flask_restful import Resource, Api, reqparse, reqparse
from .models import User
from pprint import pprint


api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    

api.add_resource(HelloWorld, '/testid')

parser = reqparse.RequestParser()

class RESTfulTest(Resource):
    def get(self, userid):
        user = User.query.filter(User.id == userid).first()
        return user._getjson()
    
    def put(self, userid):
        params = parser.parse_args()
        print("\n>>>>> input_usernameinput_username ", params)
        json = request.get_json()['data']
        print("\n>>>>>> jsonjsonjson ", json)
        ## expected values
        # >>>>> input_usernameinput_username  {'data': "{'username': 'kingkong', 'question': '2'}"}
        #>>>>>> jsonjsonjson  {'data': {'username': 'kingkong', 'question': '2'}}

        user = User.query.filter(User.id == userid).first()
        for jj in json:
            print("jjjjjjjj ", jj)
            setattr(user, jj, json[jj])
        
        print(user)
                # print(getattr(user, jj)(json[jj]))
        return "OK"

    def post(self, userid=None):
        print(userid)
        json = request.get_json()
        print("\n\n\n")
        pprint(json)
        return 201

# curl -v -H "Accept: application/json" -H "Content-type: application/json" -X PUT -d ' {"user":{"fullname":"Bob Chan","email":"bob@email.com","password":"password"}}' http://localhost:5000/restful/1
        
# parser.add_argument('data')
api.add_resource(RESTfulTest, '/restful', '/restful/<userid>')