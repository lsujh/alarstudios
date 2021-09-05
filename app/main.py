from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.constants import BASE_PATH
from app.core.config import settings
from app.db.utils import check_db_connected, check_db_disconnected
from app.views.base import views_router


def include_router(app):
    app.include_router(views_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory=str(BASE_PATH / "static")), name="static")


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.add_middleware(SessionMiddleware,
                       secret_key="some-random-string")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_router(app)
    configure_static(app)

    return app


app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()
