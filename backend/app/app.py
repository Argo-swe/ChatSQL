from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
