import json
import os
import tempfile

from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import (
    RecommendationHistory,
    User,
)

from app.schemas import (
    HomePlannerRequest,
    JewelryPlannerRequest,
    PartyPlannerRequest,
    RecommendationResponse,
)

from app.services.gemini_service import (
    gemini_service,
)


router = APIRouter()


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


def save_history(
    db: Session,
    user: User,
    planner: str,
    payload: dict,
    result: RecommendationResponse,
) -> RecommendationHistory:

    item = RecommendationHistory(

        user_id=user.id,

        planner_type=planner,

        input_json=json.dumps(
            payload,
            ensure_ascii=False,
        ),

        result_json=result.model_dump_json(),
    )

    db.add(item)

    db.commit()

    db.refresh(item)

    return item


@router.post("/generate-home")
def generate_home(
    payload: HomePlannerRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    data = payload.model_dump()

    result = gemini_service.generate(
        "home",
        data,
    )

    item = save_history(
        db,
        user,
        "home",
        data,
        result,
    )

    return {
        "history_id": item.id,
        "result": result,
    }


@router.post("/generate-party")
def generate_party(
    payload: PartyPlannerRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    data = payload.model_dump()

    result = gemini_service.generate(
        "party",
        data,
    )

    item = save_history(
        db,
        user,
        "party",
        data,
        result,
    )

    return {
        "history_id": item.id,
        "result": result,
    }


@router.post("/generate-jewelry")
async def generate_jewelry(

    budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form(...),

    metal: str = Form("Any"),

    notes: str = Form(""),

    outfit_image: UploadFile | None = File(
        None
    ),

    user: User = Depends(get_current_user),

    db: Session = Depends(get_db),
):

    payload = JewelryPlannerRequest(

        budget=budget,

        occasion=occasion,

        style=style,

        metal=metal,

        notes=notes,
    )

    data = payload.model_dump()

    image_path = None

    if outfit_image:

        if (
            outfit_image.content_type
            not in ALLOWED_IMAGE_TYPES
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, PNG or WEBP "
                    "images are allowed"
                ),
            )

        content = await outfit_image.read()

        max_bytes = (
            5 * 1024 * 1024
        )

        if len(content) > max_bytes:

            raise HTTPException(
                status_code=413,
                detail="Image is larger than 5 MB",
            )

        suffix = Path(
            outfit_image.filename
            or "outfit.jpg"
        ).suffix.lower() or ".jpg"

        fd, image_path = tempfile.mkstemp(
            prefix="pocketsmart_",
            suffix=suffix,
        )

        os.close(fd)

        Path(
            image_path
        ).write_bytes(content)

    try:

        result = gemini_service.generate(
            "jewelry",
            data,
            image_path=image_path,
        )

    finally:

        if image_path:

            Path(
                image_path
            ).unlink(
                missing_ok=True
            )

    item = save_history(
        db,
        user,
        "jewelry",
        data,
        result,
    )

    return {
        "history_id": item.id,
        "result": result,
    }


@router.get(
    "/recommendations-details/{history_id}"
)
def recommendation_details(

    history_id: int,

    user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db),
):

    item = db.get(
        RecommendationHistory,
        history_id,
    )

    if (
        not item
        or item.user_id != user.id
    ):

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return {

        "history_id": item.id,

        "planner_type": item.planner_type,

        "input": json.loads(
            item.input_json
        ),

        "result": json.loads(
            item.result_json
        ),

        "created_at": (
            item.created_at.isoformat()
            if item.created_at
            else None
        ),
    }


@router.get("/history")
def history(

    user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db),
):

    rows = (
        db.query(
            RecommendationHistory
        )
        .filter(
            RecommendationHistory.user_id
            == user.id
        )
        .order_by(
            RecommendationHistory.created_at.desc()
        )
        .all()
    )

    return [

        {
            "id": row.id,

            "planner_type": (
                row.planner_type
            ),

            "created_at": (
                row.created_at.isoformat()
                if row.created_at
                else None
            ),

            "result": json.loads(
                row.result_json
            ),
        }

        for row in rows
    ]