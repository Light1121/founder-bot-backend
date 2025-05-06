from ..base import generate_text
from .prompts import BUSINESS_PLAN_TEMPLATE


def plan_startup(user_input: str) -> str:
    """
    根据prompt 写 Startup Business Plan。
    """
    prompt = f"{BUSINESS_PLAN_TEMPLATE}\n\nUser Input: {user_input}"
    return generate_text(prompt)