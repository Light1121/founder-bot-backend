import os
import mimetypes
from google import genai
from google.genai import types

# get API Key from env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def init_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str, model: str = "gemini-2.0-flash") -> str:
    """
    通用文本生成接口。
    """
    client = init_gemini_client()
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        ),
    ]
    config = types.GenerateContentConfig(
        response_modalities=["text"],
        response_mime_type="text/plain",
    )
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config
    )
    if response.candidates:
        return response.candidates[0].content.parts[0].text
    return "No response from Gemini."


def generate_image(prompt: str, model: str = "gemini-1.5-flash") -> str:
    """
    通用图像生成接口。
    """
    client = init_gemini_client()
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        ),
    ]
    config = types.GenerateContentConfig(
        response_modalities=["image"],
        response_mime_type="image/png",
    )
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config
    ):
        cand = chunk.candidates and chunk.candidates[0].content
        if cand and cand.parts:
            inline = cand.parts[0].inline_data
            if inline:
                ext = mimetypes.guess_extension(inline.mime_type) or ".png"
                path = f"generated_image{ext}"
                with open(path, "wb") as f:
                    f.write(inline.data)
                return path
    return "No image generated."


def generate_text_stream(prompt: str, model: str = "gemini-2.0-flash"):
    """
    流式文本生成器：yield 每次从 Gemini 拉到的一小段文本。
    """
    client = init_gemini_client()
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        ),
    ]
    config = types.GenerateContentConfig(
        response_modalities=["text"],
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config
    ):
        # 每个 chunk.candidates[0].content.parts[0].text 都是一小段
        text = chunk.candidates[0].content.parts[0].text
        yield text