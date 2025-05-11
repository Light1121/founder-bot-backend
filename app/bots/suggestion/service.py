# app/bots/suggestion/service.py

from ..base import generate_text
from .prompts import SUGGESTION_TEMPLATE, RESPONSE_SUGGESTION_TEMPLATE

def get_suggestions(message: str) -> list[str]:
    """
    根据用户上一条消息，生成 4 条建议并返回列表。
    """
    # 1. get pre prompt
    prompt = SUGGESTION_TEMPLATE.format(message=message)

    # 2. from LLM respond
    result = generate_text(prompt)

    # 3. break it into list
    suggestions = []
    for line in result.splitlines():
        line = line.strip()
        if line and (dot := line.find(".")) != -1:
            content = line[dot+1:].strip()
            if content:
                suggestions.append(content)
    return suggestions[:4]

def get_response_suggestions(response: str) -> list[str]:
    """
    根据AI的回复，生成 4 条后续对话建议并返回列表。
    """
    # 1. get pre prompt
    prompt = RESPONSE_SUGGESTION_TEMPLATE.format(response=response)

    # 2. from LLM respond
    result = generate_text(prompt)

    # 3. break it into list
    suggestions = []
    for line in result.splitlines():
        line = line.strip()
        if line and (dot := line.find(".")) != -1:
            content = line[dot+1:].strip()
            if content:
                suggestions.append(content)
    return suggestions[:4]