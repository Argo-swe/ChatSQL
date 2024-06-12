from flask import request
from flask_restx import Namespace, Resource, fields
from engine.backend.index_manager import IndexManager


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

@api.route('/prompt')
class GeneratePrompt(Resource):

    def get(self):
        manager = IndexManager()

        data_dict_name = "orders"

        manager.createOrLoadIndex(data_dict_name)

        prompt = manager.promptGenerator("the surname of users who paid for all their orders with PayPal", activate_log=True)

        print(prompt)

        return { "data": prompt, "message": "OK" }, 200
