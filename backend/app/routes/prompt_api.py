from models.responses.response_dto import ResponseStatusEnum
from models.responses.string_data_response_dto import StringDataResponseDto

from fastapi import APIRouter
# from engine.backend.index_manager import IndexManager

tag = "prompt"
router = APIRouter()

# FIXME: ricollegare index manager
# manager = IndexManager()

# data_dict_name = "orders"
# manager.createOrLoadIndex(data_dict_name)

@router.get("/", tags=[tag], response_model=StringDataResponseDto)
def generate_prompt(query: str) -> StringDataResponseDto:

    if query == None:
        query = "the surname of users who paid for all their orders with PayPal"

    # prompt = manager.promptGenerator(query, activate_log=True)
    prompt = "Se mi collegate vi genero il prompt"

    print(prompt)

    # return { "data": prompt, "message": "OK" }
    return StringDataResponseDto(
        data=prompt,
        status=ResponseStatusEnum.OK.value
    )


@router.get("/debug", tags=[tag], response_model=StringDataResponseDto)
def generate_prompt(query: str) -> StringDataResponseDto:

    # FIXME: set debug method
    if query == None:
        query = "the surname of users who paid for all their orders with PayPal"

    # prompt = manager.promptGenerator(query, activate_log=True)
    prompt = "Un giorno produrrò un log di debug"

    print(prompt)

    # return { "data": prompt, "message": "OK" }
    return StringDataResponseDto(
        data=prompt,
        status=ResponseStatusEnum.OK.value
    )
