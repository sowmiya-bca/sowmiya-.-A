import json
from pathlib import Path
from typing import Any

from app.config import get_settings

from app.schemas import RecommendationResponse

from app.services.recommendation_service import (
    mock_home,
    mock_party,
    mock_jewelry,
)


settings = get_settings()


class GeminiRecommendationService:

    def __init__(self) -> None:

        self.client = None

        if (
            settings.gemini_api_key
            and not settings.mock_mode
        ):

            from google import genai

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    @property
    def live(self) -> bool:

        return self.client is not None

    def _prompt(
        self,
        planner: str,
        data: dict[str, Any],
    ) -> str:

        return f"""
You are PocketSmart AI, a budget-aware recommendation assistant.

Planner:
{planner}

User input:

{json.dumps(
    data,
    ensure_ascii=False,
    indent=2,
)}

Generate practical recommendations for an Indian user.

Respect the total budget.

Use INR amounts.

Do not invent exact live inventory, exact current prices,
ratings, reviews, stock, delivery dates, or guaranteed availability.

Estimated prices are acceptable.

Provider names should be selected from:

Amazon
Flipkart
IKEA
Swiggy
Zomato
OYO

Return ONLY the requested structured JSON.
"""

    def generate(
        self,
        planner: str,
        data: dict[str, Any],
        image_path: str | None = None,
    ) -> RecommendationResponse:

        if not self.live:

            if planner == "home":
                return mock_home(data)

            if planner == "party":
                return mock_party(data)

            return mock_jewelry(data)

        from google.genai import types

        prompt = self._prompt(
            planner,
            data,
        )

        contents: list[Any] = [
            prompt
        ]

        if image_path:

            from PIL import Image

            image = Image.open(
                image_path
            )

            contents.append(
                image
            )

            contents.append(
                """
Analyze this outfit image only for broad
colors, style and formality.

Do not identify the person.

Do not infer sensitive personal information.
"""
            )

        config = types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=(
                RecommendationResponse
                .model_json_schema()
            ),

            temperature=0.4,

            max_output_tokens=5000,
        )

        response = (
            self.client.models.generate_content(
                model=settings.gemini_model,
                contents=contents,
                config=config,
            )
        )

        return RecommendationResponse.model_validate_json(
            response.text
        )


gemini_service = GeminiRecommendationService()