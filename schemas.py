from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: str = Field(
        min_length=5,
        max_length=255,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class LoginRequest(BaseModel):

    email: str

    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


class ProductRecommendation(BaseModel):

    name: str

    category: str

    estimated_price: float = Field(
        ge=0
    )

    platform: str

    search_url: str

    why_it_fits: str

    budget_note: str


class BudgetAllocation(BaseModel):

    category: str

    amount: float = Field(
        ge=0
    )

    percentage: float = Field(
        ge=0,
        le=100,
    )


class RecommendationResponse(BaseModel):

    title: str

    summary: str

    total_budget: float = Field(
        ge=0
    )

    estimated_total: float = Field(
        ge=0
    )

    remaining_budget: float

    allocations: list[BudgetAllocation] = Field(
        default_factory=list
    )

    recommendations: list[ProductRecommendation] = Field(
        default_factory=list
    )

    tips: list[str] = Field(
        default_factory=list
    )

    disclaimer: str = (
        "Prices and availability are estimates; "
        "verify them on the linked provider before purchase."
    )


class HomePlannerRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    room: str = Field(
        min_length=2,
        max_length=80,
    )

    style: str = Field(
        min_length=2,
        max_length=80,
    )

    items: str = Field(
        min_length=2,
        max_length=2000,
    )

    notes: str = Field(
        default="",
        max_length=2000,
    )


class PartyPlannerRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    event_type: str = Field(
        min_length=2,
        max_length=80,
    )

    guests: int = Field(
        gt=0,
        le=10000,
    )

    venue: str = Field(
        min_length=2,
        max_length=200,
    )

    food: str = Field(
        default="",
        max_length=1000,
    )

    decor: str = Field(
        default="",
        max_length=1000,
    )

    notes: str = Field(
        default="",
        max_length=2000,
    )


class JewelryPlannerRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    occasion: str = Field(
        min_length=2,
        max_length=80,
    )

    style: str = Field(
        min_length=2,
        max_length=100,
    )

    metal: str = Field(
        default="Any",
        max_length=50,
    )

    notes: str = Field(
        default="",
        max_length=2000,
    )


class HistoryItem(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    planner_type: str

    created_at: str

    result: RecommendationResponse