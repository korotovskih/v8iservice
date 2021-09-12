from app.dependencies import (
    CheckInfoBasesResponse,
    GetInfoBasesResponse,
    InfoBasesCatalog,
    Settings,
    check_code,
    get_client_id,
    get_infobases_catalog,
    get_settings,
    get_wsdl,
    parse_xml_body,
)
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

router = APIRouter()


@router.get("/bases/{v8i}/WebCommonInfoBases")
async def wsdl(
    v8i: str,
    request: Request,
    catalog: InfoBasesCatalog = Depends(get_infobases_catalog),
    settings: Settings = Depends(get_settings),
):

    infobases = catalog.get_infobases(v8i)
    if not infobases:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(
        get_wsdl(location=settings.app_host, path=request.url.path),
        media_type="text/xml",
    )


@router.post("/bases/{v8i}/WebCommonInfoBases")
async def common_endpoint(
    v8i: str,
    request: Request,
    catalog: InfoBasesCatalog = Depends(get_infobases_catalog),
    settings: Settings = Depends(get_settings),
):

    infobases = catalog.get_infobases(v8i)
    if not infobases:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    body = parse_xml_body(await request.body())

    # TODO сделать нормальный парсер

    envelope = body.get("soap:Envelope")
    body = envelope.get("soap:Body")
    method, args = list(body.items())[0]

    # TODO always_pull - добавить в конфиг

    always_pull = True

    if method == "m:CheckInfoBases":

        if always_pull:
            changed = True
        else:
            changed = args["m:InfoBasesCheckCode"]["#text"] != infobases.md5_hash

        response = CheckInfoBasesResponse(
            InfoBasesChanged=changed,
            URL=request.url.path,
            location=settings.app_host,
        )

    elif method == "m:GetInfoBases":

        if always_pull:
            code = check_code()
        else:
            code = infobases.md5_hash

        client_id = args["m:ClientID"]["#text"]
        if client_id == "00000000-0000-0000-0000-000000000000":
            client_id = get_client_id()

        response = GetInfoBasesResponse(
            ClientID=client_id,
            InfoBasesCheckCode=code,
            InfoBases=infobases.content,
            location=settings.app_host,
        )

    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    return Response(response.envelope(), media_type="application/soap+xml")
