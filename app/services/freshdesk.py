import httpx
import openai

FRESHDESK_DOMAIN = "yourdomain.freshdesk.com"
FRESHDESK_API_KEY = "your_api_key"
OPENAI_API_KEY = "your_openai_api_key"

openai.api_key = OPENAI_API_KEY

def fetch_kb_articles():
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/solutions/articles"
    response = httpx.get(url, auth=(FRESHDESK_API_KEY, "X"))
    if response.status_code == 200:
        return response.json()
    return []

def create_support_ticket(subject: str, description: str, email: str):
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets"
    payload = {
        "subject": subject,
        "description": description,
        "email": email,
        "priority": 1,
        "status": 2
    }
    response = httpx.post(url, json=payload, auth=(FRESHDESK_API_KEY, "X"))
    return response.json()

def get_ai_response(user_message: str, kb_articles: list) -> str:
    context = "You are FreshBot AI, a smart support bot that helps users by referencing articles from the knowledge base.
"
    context += "If you don't find an answer in the knowledge base, kindly let the user know.

"
    context += "Here are some knowledge base articles:
"
    for article in kb_articles[:5]:
        context += f"- {article.get('title')}
"

    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": user_message}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200,
        temperature=0.5,
    )

    return response.choices[0].message["content"].strip()
