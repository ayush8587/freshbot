from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.freshdesk import fetch_kb_articles, create_support_ticket, get_ai_response

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def handle_chat(req: ChatRequest):
    user_msg = req.message.strip()
    articles = fetch_kb_articles()
    reply = get_ai_response(user_msg, articles)

    if "create a ticket" in user_msg.lower() or "support ticket" in user_msg.lower():
        create_support_ticket(subject="User Support Request", description=user_msg, email=req.user_email)
        return ChatResponse(reply=f"{reply} — I've also created a support ticket for you.", ticket_created=True)

    return ChatResponse(reply=reply)
