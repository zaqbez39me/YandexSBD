from app.router import router

from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)

    return application


app = get_application()
