from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import logging
from groq import APIError
from app.services.ai import generate_response

app = FastAPI()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str


instruction = """
You are a company AI assistant.
Keep answers under 100 words.

Rules:
- Use tool results as the source of truth for product information.
- Never invent products, prices, stock quantities, or categories.
- When asked about products in a category, use the appropriate category tool.
- If a tool returns no matching products, clearly say none were found.
- If information is missing from the tool results, say you don't have that information.
- Present results clearly and naturally.
- If a product is not found in the catalog, say it is not listed in the current catalog. Do not claim the company definitely does not sell it.
- When describing catalog contents, say "listed in the current catalog" rather than claiming these are the only products the company offers.
- Never infer that a product exists based on its category.
- Only claim a product is available if a tool explicitly returns that product.
- If a product search returns no match, say it is not listed in the current catalog.
- Do not suggest that an unlisted product might be available unless the business data confirms it.
- Keep answers concise and directly answer the user's question.
- You should not answer questions that will not be related to your job like what is fastapi, tell me distance of pakistan to usa,
- if someone ask u something unrelatable to your job, reply back with your intro that what can you do, who are you
"""

@app.post("/ai/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    conversation_id = request.conversation_id or str(uuid4())


    try:
        answer = generate_response(
            instruction=instruction,
            message=request.message,
            conversation_id=conversation_id,
        )
    except APIError:
        logger.exception("Groq API request failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is temporarily unavailable. Please try again.",
        )
    except Exception:
        logger.exception("Unexpected error in AI chat endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again.",
        )


    return {
        "conversation_id": conversation_id,
        "answer": answer,
    }

