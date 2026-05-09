from fastapi import FastAPI

from models.schemas import (
    ChatRequest,
    ChatResponse
)

from services.chat_logic import (
    process_chat
)

app = FastAPI()


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    response = process_chat(
        request.messages
    )

    return response