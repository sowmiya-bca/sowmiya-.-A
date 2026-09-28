from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from fastapi.middleware.trustedhost import (
    TrustedHostMiddleware,
)

from starlette.middleware.sessions import (
    SessionMiddleware,
)

from fastapi.staticfiles import (
    StaticFiles,
)

from app.config import get_settings

from app.database import init_db

from app.routes import (
    api_routes,
    auth_routes,
    pages,
    planner_routes,
)


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(

    title=settings.app_name,

    version="1.0.0",

    description=(
        "Budget-aware AI recommendation "
        "assistant for home, party and "
        "jewelry planning."
    ),

    lifespan=lifespan,
)


app.add_middleware(
    SessionMiddleware,

    secret_key=settings.secret_key,

    max_age=8 * 60 * 60,

    same_site="lax",

    https_only=False,
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=settings.cors_origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.mount(

    "/static",

    StaticFiles(
        directory="app/static"
    ),

    name="static",
)


app.include_router(
    pages.router
)

app.include_router(
    auth_routes.router
)

app.include_router(
    planner_routes.router
)

app.include_router(
    api_routes.router
)