from app.dependencies import (
    InfoBasesCatalog,
    check_code,
    get_client_id,
    get_infobases_catalog,
)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, PlainTextResponse

router = APIRouter()
root = "/bases/{v8i}"


@router.head(f"{root}/WebCommonInfoBases/")
async def head(v8i: str):
    pass


@router.get(f"{root}/CheckInfoBases/", response_class=JSONResponse)
async def check(
    v8i: str,
    ClientID: str = "00000000-0000-0000-0000-000000000000",
    InfoBasesCheckCode: str = "",
    catalog: InfoBasesCatalog = Depends(get_infobases_catalog),
):

    infobases = catalog.get_infobases(v8i)
    if not infobases:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # TODO always_pull - добавить в конфиг

    always_pull = True
    if always_pull:
        changed = True
    else:
        changed = InfoBasesCheckCode != infobases.md5_hash

    # return {"root": {"InfoBasesChanged": changed}}
    return JSONResponse({"InfoBasesChanged": changed}, status_code=201)


@router.get(f"{root}/GetInfoBases/", response_class=JSONResponse)
async def get(
    v8i: str,
    ClientID: str = "00000000-0000-0000-0000-000000000000",
    InfoBasesCheckCode: str = "",
    catalog: InfoBasesCatalog = Depends(get_infobases_catalog),
):

    infobases = catalog.get_infobases(v8i)
    if not infobases:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    client_id = ClientID
    if client_id == "00000000-0000-0000-0000-000000000000":
        client_id = get_client_id()

    # TODO always_pull - добавить в конфиг

    always_pull = True
    if always_pull:
        code = check_code()
    else:
        code = infobases.md5_hash

    f = {
        "root": {
            "ClientID": client_id,
            "InfoBases": infobases.content,
            "InfoBasesCheckCode": code,
        }
    }
    return {
        "ClientID": client_id,
        "InfoBases": infobases.content,
        "InfoBasesCheckCode": code,
    }
