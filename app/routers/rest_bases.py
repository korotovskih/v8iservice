from fastapi import APIRouter

router = APIRouter()


@router.get("/bases/WebCommonInfoBases/CheckInfoBases/")
async def check_ib(ClientID: str, InfoBasesCheckCode: str):
    # TODO сделать когда будет документация
    return {
        "InfoBasesChanged": True,
        "URL": "/bases/WebCommonInfoBases1111/GetInfoBases/",
    }


@router.get("/bases/WebCommonInfoBases/GetInfoBases/")
async def get_ib(ClientID: str, InfoBasesCheckCode: str):
    # TODO сделать когда будет документация
    with open("doc/default.v8i", encoding="utf-8-sig") as f:
        v8i = f.read()

    client_id = "af822745-ab05-42ac-b826-80d422afb4b7"
    checkcode = "4c73ecaa-8641-4ad1-a730-fd884fa5aeb0"

    json = {"ClientID": client_id, "InfoBasesCheckCode": checkcode, "InfoBases": v8i}

    return json
