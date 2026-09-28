from urllib.parse import quote_plus


PROVIDERS = {

    "amazon": (
        "Amazon",
        "https://www.amazon.in/s?k={query}",
    ),

    "flipkart": (
        "Flipkart",
        "https://www.flipkart.com/search?q={query}",
    ),

    "ikea": (
        "IKEA",
        "https://www.ikea.com/in/en/search/?q={query}",
    ),

    "swiggy": (
        "Swiggy",
        "https://www.swiggy.com/search?query={query}",
    ),

    "zomato": (
        "Zomato",
        "https://www.zomato.com/search?query={query}",
    ),

    "oyo": (
        "OYO",
        "https://www.oyorooms.com/search?location={query}",
    ),
}


def provider_link(
    provider_key: str,
    query: str,
) -> tuple[str, str]:

    name, template = PROVIDERS.get(
        provider_key,
        PROVIDERS["amazon"],
    )

    return (
        name,
        template.format(
            query=quote_plus(query)
        ),
    )


def provider_for_category(
    category: str,
) -> str:

    category = category.lower()

    if any(
        x in category
        for x in (
            "food",
            "catering",
            "restaurant",
        )
    ):
        return "zomato"

    if any(
        x in category
        for x in (
            "venue",
            "hotel",
            "stay",
        )
    ):
        return "oyo"

    if any(
        x in category
        for x in (
            "furniture",
            "home",
            "decor",
            "lighting",
        )
    ):
        return "ikea"

    if any(
        x in category
        for x in (
            "jewelry",
            "jewellery",
            "necklace",
            "earring",
            "bracelet",
        )
    ):
        return "amazon"

    return "flipkart"