
from pydantic import BaseModel, ConfigDict, Field


class CalculateTotalInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    price: float = Field(ge=0)
    quantity: int = Field(ge=1)

class SearchProductInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)

class SearchProductsByCategoryInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: str = Field(min_length=1, max_length=100)

class ListCategoriesInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


def search_products(
    max_price: float | None = None,
    wireless: bool | None = None,
    use_case: str | None = None,
) -> list[dict]:
    results = []

    for product in products:
        specifications = product.get("specifications", {})

        if max_price is not None and product["price"] > max_price:
            continue

        if (
            wireless is not None
            and specifications.get("wireless") != wireless
        ):
            continue

        if (
            use_case is not None
            and use_case.lower()
            not in [case.lower() for case in specifications.get("use_case", [])]
        ):
            continue

        results.append(product)

    return results

def search_products_by_category(category: str) -> dict:
    query = category.strip().lower()

    if not query:
        return {
            "status": "invalid_query",
            "products": [],
            "message": "Please provide a category.",
        }

    matches = [
        product
        for product in products
        if product["category"].lower() == query
    ]

    if matches:
        return {
            "status": "found",
            "products": matches,
        }

    return {
        "status": "not_found",
        "products": [],
        "message": "No products found in that category.",
    }

def calculate_total(price: float, quantity: int) -> float:
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    return price * quantity

def list_categories() -> dict:
    categories = sorted({
        product["category"]
        for product in products
    })

    return {
        "status": "success",
        "categories": categories,
    }

products = [
    {
        "id": 1,
        "name": "Keyboard",
        "category": "Accessories",
        "price": 50.0,
        "stock": 10,
        "specifications": {
            "wireless": False,
            "connection": "USB",
            "backlit": True,
            "use_case": ["typing", "office"],
        },
    },
    {
        "id": 2,
        "name": "Wireless Gaming Mouse",
        "category": "Accessories",
        "price": 35.0,
        "stock": 12,
        "specifications": {
            "wireless": True,
            "connection": "2.4GHz USB receiver",
            "dpi": 16000,
            "use_case": ["gaming"],
        },
    },
    {
        "id": 3,
        "name": "Monitor",
        "category": "Displays",
        "price": 200.0,
        "stock": 5,
        "specifications": {
            "size_inches": 27,
            "resolution": "1440p",
            "refresh_rate_hz": 144,
            "use_case": ["gaming", "office"],
        },
    },
]

Tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_total",
            "description": "Calculate the total price of a product order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "price": {
                        "type": "number",
                        "description": "Price per item",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Number of items",
                    },
                },
                "required": ["price", "quantity"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_product",
            "description": "Search the product catalog by product name or partial name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The product name or search phrase."
                    }
                },
                "required": ["name"],
                "additionalProperties": False
            }
        }
    }, 
    {
        "type": "function",
        "function": {
            "name": "list_categories",
            "description": (
                "Return the categories of products available "
                "in the catalog. Use this when the user asks "
                "what types of products the business sells."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "search_products_by_category",
        "description": (
            "Find and return all products in a specified category. "
            "Use this when the user asks which products belong to a category."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "The product category to search for."
                }
            },
            "required": ["category"],
            "additionalProperties": False
        }
    }
}
]

available_functions = {
    "calculate_total": calculate_total,
    "search_producs" : search_products,
    "list_categories" : list_categories,
    "search_products_by_category": search_products_by_category,
}

tool_input_models = {
    "calculate_total": CalculateTotalInput,
    "search_product": SearchProductInput,
    "search_products_by_category": SearchProductsByCategoryInput,
    "list_categories": ListCategoriesInput,
}

