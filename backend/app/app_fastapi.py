#from flask import Flask
#from flask_restx import Api
#from flask_cors import CORS
import os

#from routes.test import api as test_namespace

# Try loading an evn var, or go to default.
#which_env_file = os.environ.get('WELCOME', '.env-* did not load')

# api = Api(
#     title="ChatSQL API",
#     version="1.0",
#     description="API for ChatSQL",
#     doc="/api-doc"
# )

# api.add_namespace(test_namespace, path='/api/test')

# app = Flask(__name__)
# app.config["RESTX_MASK_SWAGGER"]=False
# CORS(app)
# api.init_app(app)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from domain.info import Info
from routes.dictionaries_api import router as dictionaries_router
from routes.prompt_api import router as prompt_router

app = FastAPI()

app.include_router(dictionaries_router, prefix="/api/dictionary")
app.include_router(prompt_router, prefix="/api/prompt")

app.add_middleware(CORSMiddleware,
                   allow_credentials=True,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

@app.get("/")
async def main():
    return {"message": "Hello World"}

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
