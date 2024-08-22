import logging
from configuration import Configuration
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.openapi import simplify_operation_ids
from tools.log_filter import EndpointFilter

from routes.dictionaries_api import dictionaries_router
from routes.prompt_api import prompt_router
from routes.login_api import login_router

tags_metadata = [
    {"name": "dictionary", "description": "Operations with dictionaries"},
    {"name": "prompt", "description": "Operations to generate prompt"},
    {"name": "login", "description": "Operations to authenticate user"},
]

app = FastAPI(openapi_tags=tags_metadata)

configuration = Configuration()

app.include_router(dictionaries_router(configuration), prefix="/api/dictionary")
app.include_router(prompt_router(configuration), prefix="/api/prompt")
app.include_router(login_router(configuration), prefix="/api/login")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define excluded endpoints
excluded_endpoints = ["/healthcheck", "/openapi.json"]

# Add filter to the logger
logging.getLogger("uvicorn.access").addFilter(EndpointFilter(excluded_endpoints))


@app.get("/", summary="Root endpoint")
async def main():
    """
    Return a simple greeting message.

    This endpoint can be used to verify that the API is reachable.
    """
    return {"message": "Hello World"}


@app.get("/healthcheck", summary="Health check endpoint")
async def healthcheck():
    """
    Check the health status of the API.

    Returns a status message indicating whether the API is running.
    """
    return {"status": "running"}


simplify_operation_ids(app)


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
