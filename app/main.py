from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.rest_bases import router as rest_bases_router
from app.routers.soap_bases import router as soap_bases_router


def get_application() -> FastAPI:

    application = FastAPI()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(rest_bases_router, prefix="/v1/rest")
    application.include_router(soap_bases_router, prefix="/v1/soap")

    return application


app = get_application()
