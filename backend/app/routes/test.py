from flask import request
from flask_restx import Namespace, Resource, fields

api = Namespace('Tests',"APIs related to test modules")

@api.route('/')
class Test(Resource):

    def get(self):
        return {"data":[], "message":"OK"}, 200

@api.route('/<int:test_id>')
class CheckTest(Resource):

    def get(self, test_id):
        if test_id <= 5:
            return {"data": f"test #{test_id}", "message":"OK"}, 200

        return {"data":{}, "message":"Test id is greater than 4"}, 404

    def post(self, test_id):
        if test_id <= 5:
            return {"data": f"test #{test_id}", "message":"OK"}, 200

        return {"data":{}, "message":"Test id is greater than 4"}, 404
