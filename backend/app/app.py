from flask import Flask
from flask_restx import Api
from flask_cors import CORS
# import os

from routes.test import api as test_namespace

# Try loading an evn var, or go to default.
#which_env_file = os.environ.get('WELCOME', '.env-* did not load')

api = Api(
    title="ChatSQL API",
    version="1.0",
    description="API for ChatSQL",
    doc="/api-doc"
)

api.add_namespace(test_namespace, path='/api/test')

app = Flask(__name__)
app.config["RESTX_MASK_SWAGGER"]=False
CORS(app)
api.init_app(app)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
