# 文件: app/bots/gemini_service.py
import os
import mimetypes
from google import genai
from google.genai import types

# 读取环境变量
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def init_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)

def list_available_models():
    client = init_gemini_client()
    models = client.models.list_models()
    for model in models:
        print(model)

def generate_text(prompt: str) -> str:
    """
    调用 Gemini 生成文本内容。
    """
    # 初始化
    client = init_gemini_client()
    model_name = "gemini-1.5-pro"

    # 准备对话内容
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        ),
    ]

    # 生成配置
    generate_config = types.GenerateContentConfig(
        response_modalities=["text"],
        response_mime_type="text/plain",
    )

    # 调用API，获取结果
    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=generate_config
    )

    # 解析响应
    if response.candidates and len(response.candidates) > 0:
        # 返回第一候选的文本
        return response.candidates[0].content.parts[0].text
    else:
        return "No response from Gemini."

def generate_image(prompt: str, file_name_prefix="generated_image") -> str:
    """
    调用 Gemini 生成图像内容，并将图像保存到本地文件。
    返回保存的文件路径。
    """
    client = init_gemini_client()
    model_name = "gemini-1.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        ),
    ]

    generate_config = types.GenerateContentConfig(
        response_modalities=["image"],
        # onlt output image
        response_mime_type="image/png",
    )

    # 这里使用流式获取方式
    for chunk in client.models.generate_content_stream(
        model=model_name,
        contents=contents,
        config=generate_config
    ):
        # 检查是否有生成的图像
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue

        part_data = chunk.candidates[0].content.parts[0].inline_data
        if part_data:
            # 根据 MIME 类型推断文件后缀
            ext = mimetypes.guess_extension(part_data.mime_type) or ".png"
            file_path = f"{file_name_prefix}{ext}"

            # 保存文件
            with open(file_path, "wb") as f:
                f.write(part_data.data)

            return file_path

    # 如果没有任何图像内容返回
    return "No image generated."