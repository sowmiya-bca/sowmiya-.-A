from fastapi import APIRouter

from app.services.gemini_service import (
    gemini_service,
)


router = APIRouter()


@router.get("/health")
def health():

    return {
        "status": "ok",
        "ai_mode": (
            "gemini"
            if gemini_service.live
            else "mock"
        ),
    }


@router.post("/startup")
def startup():

    return {
        "status": "ready",
        "ai_mode": (
            "gemini"
            if gemini_service.live
            else "mock"
        ),
    }