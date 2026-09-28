from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.database import get_db
from app.models import User
from app.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)


router = APIRouter()


@router.post("/register")
def register(
    payload: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db),
):

    existing_user = db.scalar(
        select(User).where(
            User.email == payload.email
        )
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        )

    user = User(
        name=payload.name.strip(),
        email=payload.email,
        password_hash=hash_password(
            payload.password
        ),
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    token = create_access_token(
        user.id
    )

    request.session[
        "access_token"
    ] = token

    return {
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):

    user = db.scalar(
        select(User).where(
            User.email == payload.email
        )
    )

    if (
        not user
        or not verify_password(
            payload.password,
            user.password_hash,
        )
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        user.id
    )

    request.session[
        "access_token"
    ] = token

    return TokenResponse(
        access_token=token
    )


@router.post("/logout")
def logout(request: Request):

    request.session.clear()

    return {
        "message": "Logged out successfully"
    }


@router.post(
    "/token",
    response_model=TokenResponse,
)
def token(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):

    return login(
        payload,
        request,
        db,
    )


@router.get("/session-info")
def session_info(request: Request):

    return {
        "logged_in": bool(
            request.session.get(
                "access_token"
            )
        ),
        "has_session": bool(
            request.session
        ),
    }


@router.get("/session-data")
def session_data(
    request: Request,
    db: Session = Depends(get_db),
):

    from app.auth import get_optional_user

    user = get_optional_user(
        request,
        db=db,
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Login required",
        )

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
    }