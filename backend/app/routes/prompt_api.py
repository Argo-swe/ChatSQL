from fastapi import APIRouter
from engine.backend.index_manager import IndexManager

tag = "prompt"
router = APIRouter()

manager = IndexManager()


@router.get("/", tags=[tag], response_model=str)
def generate_prompt(query: str) -> str:

    data_dict_name = "orders"

    manager.createOrLoadIndex(data_dict_name)

    prompt = manager.promptGenerator("the surname of users who paid for all their orders with PayPal", activate_log=True)

    print(prompt)

    return { "data": prompt, "message": "OK" }
