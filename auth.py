from datetime import (
    datetime,
    timedelta,
    timezone,
)

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from jose import (
    JWTError,
    jwt,
)

from sqlalchemy.orm import Session

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app.config import get_settings
from app.database import get_db
from app.models import User


settings = get_settings()

bearer = HTTPBearer(
    auto_error=False
)


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    return check_password_hash(
        password_hash,
        password,
    )


def create_access_token(
    user_id: int,
) -> str:

    expires = (
        datetime.now(timezone.utc)
        + timedelta(hours=8)
    )

    payload = {
        "sub": str(user_id),
        "exp": expires,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm="HS256",
    )


def _user_from_token(
    token: str,
    db: Session,
) -> User:

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
        )

        user_id = int(
            payload.get("sub", "")
        )

    except (
        JWTError,
        ValueError,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.get(
        User,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:

    token = None

    if credentials is not None:
        token = credentials.credentials

    if not token:
        token = request.session.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login required",
        )

    return _user_from_token(
        token,
        db,
    )


def get_optional_user(
    request: Request,
) -> User | None:

    token = request.session.get(
        "access_token"
    )

    if not token:
        return None

    from app.database import SessionLocal

    db = SessionLocal()

    try:
        return _user_from_token(
            token,
            db,
        )

    except HTTPException:
        return None

    finally:
        db.close()