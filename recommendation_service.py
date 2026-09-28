from app.schemas import (
    BudgetAllocation,
    ProductRecommendation,
    RecommendationResponse,
)

from app.services.provider_catalog import (
    provider_for_category,
    provider_link,
)


def _product(
    name: str,
    category: str,
    price: float,
    why: str,
) -> ProductRecommendation:

    provider = provider_for_category(
        category
    )

    platform, url = provider_link(
        provider,
        name,
    )

    return ProductRecommendation(
        name=name,
        category=category,
        estimated_price=round(
            price,
            2,
        ),
        platform=platform,
        search_url=url,
        why_it_fits=why,
        budget_note=(
            "Estimated price; verify current "
            "price, stock, delivery and seller "
            "details on the provider."
        ),
    )


def mock_home(
    data: dict,
) -> RecommendationResponse:

    budget = float(
        data["budget"]
    )

    base = max(
        budget / 5,
        500,
    )

    recommendations = [

        _product(
            f"{data['style']} ceiling light",
            "Lighting",
            base * 0.55,
            "Adds focused ambient lighting while staying within the plan.",
        ),

        _product(
            f"Modern {data['room']} storage unit",
            "Furniture",
            base * 1.35,
            "Provides practical storage with a flexible style.",
        ),

        _product(
            f"{data['style']} accent decor set",
            "Decor",
            base * 0.45,
            "Adds visual character without using a large part of the budget.",
        ),

        _product(
            f"Comfortable {data['room']} seating",
            "Furniture",
            base * 1.65,
            "Balances everyday comfort with the selected style.",
        ),
    ]

    total = sum(
        item.estimated_price
        for item in recommendations
    )

    return RecommendationResponse(

        title=f"{data['room']} budget plan",

        summary=(
            f"A {data['style']} setup "
            f"built around a "
            f"₹{budget:,.0f} budget."
        ),

        total_budget=budget,

        estimated_total=total,

        remaining_budget=budget - total,

        allocations=[

            BudgetAllocation(
                category="Furniture",
                amount=budget * 0.45,
                percentage=45,
            ),

            BudgetAllocation(
                category="Lighting",
                amount=budget * 0.15,
                percentage=15,
            ),

            BudgetAllocation(
                category="Decor",
                amount=budget * 0.20,
                percentage=20,
            ),

            BudgetAllocation(
                category="Contingency",
                amount=budget * 0.20,
                percentage=20,
            ),
        ],

        recommendations=recommendations,

        tips=[
            "Measure the room before ordering.",
            "Keep a contingency amount for delivery and installation.",
            "Compare the same item across providers before purchasing.",
        ],
    )


def mock_party(
    data: dict,
) -> RecommendationResponse:

    budget = float(
        data["budget"]
    )

    guests = int(
        data["guests"]
    )

    food_budget = budget * 0.45
    venue_budget = budget * 0.25
    decor_budget = budget * 0.15
    reserve = budget * 0.15

    recommendations = [

        _product(
            f"{data['event_type']} catering for {guests} guests",
            "Food",
            food_budget,
            "Uses a proportional food allocation based on guest count.",
        ),

        _product(
            f"{data['venue']} event venue",
            "Venue",
            venue_budget,
            "Keeps venue spending controlled within the overall event budget.",
        ),

        _product(
            f"{data['event_type']} decoration package",
            "Decor",
            decor_budget,
            "Covers basic visual decoration without exhausting the budget.",
        ),
    ]

    return RecommendationResponse(

        title=f"{data['event_type']} party budget plan",

        summary=(
            f"Planning for {guests} guests "
            f"with a ₹{budget:,.0f} total budget."
        ),

        total_budget=budget,

        estimated_total=budget - reserve,

        remaining_budget=reserve,

        allocations=[

            BudgetAllocation(
                category="Food/Catering",
                amount=food_budget,
                percentage=45,
            ),

            BudgetAllocation(
                category="Venue",
                amount=venue_budget,
                percentage=25,
            ),

            BudgetAllocation(
                category="Decoration",
                amount=decor_budget,
                percentage=15,
            ),

            BudgetAllocation(
                category="Reserve",
                amount=reserve,
                percentage=15,
            ),
        ],

        recommendations=recommendations,

        tips=[
            "Confirm per-person food pricing before booking.",
            "Ask the venue about taxes and service charges.",
            "Keep the reserve untouched until the final booking stage.",
        ],
    )


def mock_jewelry(
    data: dict,
) -> RecommendationResponse:

    budget = float(
        data["budget"]
    )

    recommendations = [

        _product(
            f"{data['style']} necklace in {data['metal']}",
            "Jewelry",
            budget * 0.40,
            "A statement piece can anchor the overall occasion look.",
        ),

        _product(
            f"{data['style']} matching earrings in {data['metal']}",
            "Jewelry",
            budget * 0.25,
            "Adds coordination without using the entire budget.",
        ),

        _product(
            f"Minimal {data['style']} bracelet",
            "Jewelry",
            budget * 0.15,
            "A lighter accessory option for balance.",
        ),
    ]

    total = sum(
        item.estimated_price
        for item in recommendations
    )

    return RecommendationResponse(

        title=f"{data['occasion']} jewelry plan",

        summary=(
            f"Jewelry suggestions for a "
            f"{data['style']} preference "
            f"within ₹{budget:,.0f}."
        ),

        total_budget=budget,

        estimated_total=total,

        remaining_budget=budget - total,

        allocations=[

            BudgetAllocation(
                category="Necklace",
                amount=budget * 0.40,
                percentage=40,
            ),

            BudgetAllocation(
                category="Earrings",
                amount=budget * 0.25,
                percentage=25,
            ),

            BudgetAllocation(
                category="Bracelet",
                amount=budget * 0.15,
                percentage=15,
            ),

            BudgetAllocation(
                category="Reserve",
                amount=budget * 0.20,
                percentage=20,
            ),
        ],

        recommendations=recommendations,

        tips=[
            "Use the uploaded outfit image only as a style/color reference.",
            "Check material, dimensions and seller details before purchase.",
            "Keep accessories coordinated rather than matching every item exactly.",
        ],
    )