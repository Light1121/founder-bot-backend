# app/bots/general_chat/service.py
from ..base import generate_text

def chat_general(user_input: str) -> str:
    # 直接把 user_input 当做 prompt 传给 generate_text
    return generate_text(user_input)