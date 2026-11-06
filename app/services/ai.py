import json
import logging

from groq import Groq
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.core.config import settings


class CalculateTotalInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_id: int = Field(ge=1)
    quantity: int = Field(ge=1)

class SearchProductsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    max_price: float | None = Field(default=None, ge=0)
    wireless: bool | None = None
    use_case: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

class SearchProductsByCategoryInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: str = Field(min_length=1, max_length=100)

class ListCategoriesInput(BaseModel):
    model_config = ConfigDict(extra="forbid")



def search_products(
    query: str | None = None,
    max_price: float | None = None,
    wireless: bool | None = None,
    use_case: str | None = None,
) -> list[dict]:
    results = []

    for product in products:
        specifications = product.get("specifications", {})

        if query is not None:
            searchable_text = (
                f"{product['name']} {product['category']}"
            ).lower()

            if query.lower() not in searchable_text:
                continue

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
            not in [
                case.lower()
                for case in specifications.get("use_case", [])
            ]
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

def calculate_total(product_id: int, quantity: int) -> dict:
    product = next(
        (item for item in products if item["id"] == product_id),
        None,
    )

    if product is None:
        return {
            "status": "not_found",
            "message": "Product not found in the current catalog.",
        }

    total = product["price"] * quantity

    return {
        "status": "success",
        "product_id": product["id"],
        "product_name": product["name"],
        "unit_price": product["price"],
        "quantity": quantity,
        "total": round(total, 2),
    }

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
            "description": (
                "Calculate the total price for a product using its catalog ID "
                "and requested quantity. The backend retrieves the authoritative "
                "price from the current product catalog. Never supply a price."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "The ID of the product in the catalog.",
                    },
                    "quantity": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "The number of units requested.",
                    },
                },
                "required": ["product_id", "quantity"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": (
                "Search the product catalog by product name or keyword, "
                "maximum price, wireless specification, and intended use. "
                "Use this tool when the user asks to find or search for "
                "a specific product, such as a mouse, keyboard, or monitor."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": ["string", "null"],
                        "minLength": 1,
                        "maxLength": 100,
                        "description": (
                            "Product name or keyword, such as mouse, keyboard, "
                            "or monitor. Use null if no keyword is specified."
                        ),
                    },
                    "max_price": {
                        "type": ["number", "null"],
                        "minimum": 0,
                        "description": "Maximum product price. Use null if no price limit is specified.",
                    },
                    "wireless": {
                        "type": ["boolean", "null"],
                        "description": "Whether the product must be wireless. Use null if the user has no wireless preference.",
                    },
                    "use_case": {
                        "type": ["string", "null"],
                        "minLength": 1,
                        "maxLength": 100,
                        "description": "Intended use, such as gaming or office. Use null if no use case is specified.",
                    },

                },
                "required": [],
                "additionalProperties": False,
            },
        },
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
    "search_products": search_products,
    "list_categories": list_categories,
    "search_products_by_category": search_products_by_category,
}

tool_input_models = {
    "calculate_total": CalculateTotalInput,
    "search_products": SearchProductsInput,
    "search_products_by_category": SearchProductsByCategoryInput,
    "list_categories": ListCategoriesInput,
}

conversation_store: dict[str, list[dict]] = {}

client = Groq(api_key=settings.groq_api_key)

logger = logging.getLogger(__name__)

def generate_response(
    instruction: str,
    message: str,
    conversation_id: str,
) -> str:
    if conversation_id not in conversation_store:
        conversation_store[conversation_id] = [
            {"role": "system", "content": instruction}
        ]

    messages = conversation_store[conversation_id]
    messages.append({"role": "user", "content": message})

    tool_rounds = 0
    max_tool_rounds = 5

    while True:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=Tools,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:
            answer = assistant_message.content or ""
            messages.append({
                "role": "assistant",
                "content": answer,
            })
            return answer

        if tool_rounds >= max_tool_rounds:
            return (
                "I couldn't complete the request within "
                "the tool-call limit."
            )

        tool_rounds += 1
        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function = available_functions.get(function_name)

            if function is None:
                result = {"error": "Unknown function"}

            else:
                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    input_model = tool_input_models.get(
                        function_name
                    )

                    if input_model is None:
                        raise LookupError(
                            "Tool has no input validation model"
                        )

                    validated = input_model(**arguments)  #Validation of arguments

                    arguments = validated.model_dump()

                except (
                    json.JSONDecodeError,
                    ValidationError,
                    TypeError,
                    LookupError,
                ) as exc:
                    logger.warning(
                        "Tool argument validation failed for %s (%s)",
                        function_name,
                        type(exc).__name__,
                    )

                    result = {
                        "error": (
                            "Invalid tool arguments. Check the "
                            "required fields and their values."
                        )
                    }

                else:
                    try:
                        logger.info(
                            "Executing tool: %s",
                            function_name,
                        )

                        result = function(**arguments)

                    except Exception:
                        logger.exception(
                            "Tool execution failed for %s",
                            function_name,
                        )

                        result = {
                            "error": (
                                "The tool could not complete the "
                                "request due to an internal error."
                            )
                        }

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })
