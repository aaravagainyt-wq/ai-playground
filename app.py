# app.py

from fastapi import FastAPI
from pydantic import BaseModel
from gpt4all import GPT4All
from safety import is_safe
from utils import log_message, format_history

app = FastAPI()

# Load GPT4All free model (download first from https://gpt4all.io)
ai_model = GPT4All("ggml-gpt4all-j-v1.3-groovy")

SYSTEM_RULES = """
You are an AI researcher in a safe environment.
STRICT RULES:
- Never promote harm or violence
- Never give unsafe, illegal, or offensive advice
- Always respect humans
- If unsure or unsafe, refuse politely
"""

class ChatStart(BaseModel):
    topic: str
    turns: int = 6  # max 20 recommended

@app.post("/start")
def start_chat(data: ChatStart):
    topic = data.topic
    max_turns = min(data.turns, 20)

    log = []
    history_text = ""
    ai_message = f"Let's discuss safely: {topic}"

    for i in range(max_turns):
        speaker = "AI-1" if i % 2 == 0 else "AI-2"

        prompt = f"{SYSTEM_RULES}\n{speaker}, continue discussion:\nHistory:\n{history_text}\n{ai_message}"

        # Generate AI reply
        reply = ai_model.generate(prompt, max_tokens=200)

        # Safety check
        if not is_safe(reply):
            reply = "[BLOCKED BY SAFETY FILTER]"

        # Log and update history
        log = log_message(log, speaker, reply)
        history_text = format_history(log)
        ai_message = reply

    return {"topic": topic, "conversation": log}
