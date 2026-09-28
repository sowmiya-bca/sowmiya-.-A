from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth import get_optional_user


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": get_optional_user(request),
        },
    )


@router.get(
    "/login",
    response_class=HTMLResponse,
)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "user": get_optional_user(request),
        },
    )


@router.get(
    "/register",
    response_class=HTMLResponse,
)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "user": get_optional_user(request),
        },
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": get_optional_user(request),
        },
    )


@router.get(
    "/planner/{planner}",
    response_class=HTMLResponse,
)
def planner_page(
    request: Request,
    planner: str,
):

    if planner not in {
        "home",
        "party",
        "jewelry",
    }:
        raise HTTPException(
            status_code=404,
            detail="Planner not found",
        )

    return templates.TemplateResponse(
        request=request,
        name=f"{planner}_planner.html",
        context={
            "user": get_optional_user(request),
        },
    )


@router.get(
    "/history-page",
    response_class=HTMLResponse,
)
def history_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "user": get_optional_user(request),
        },
    )