# 文件: app/bots/gemini_controller.py
from flask_restx import Namespace, Resource, fields
from flask import request

# 导入我们在 service.py 中写好的逻辑
from .service import generate_text, generate_image

api = Namespace("gemini", description="Gemini AI Endpoints")

# 定义一下请求和响应的数据模型(可选)
text_model = api.model("TextRequest", {
    "prompt": fields.String(required=True)
})

image_model = api.model("ImageRequest", {
    "prompt": fields.String(required=True)
})

@api.route("/text")
class GeminiTextResource(Resource):
    @api.expect(text_model)
    def post(self):
        """
        POST /api/gemini/text
        传入 prompt 返回 Gemini 生成的文本
        """
        data = request.json
        prompt = data.get("prompt", "")
        if not prompt:
            return {"error": "No prompt provided."}, 400
        
        # 调用 service
        response_text = generate_text(prompt)
        return {"response": response_text}, 200
    
@api.route("/report")
class GeminiTextResource(Resource):
    @api.expect(text_model)
    def post(self):
        """
        POST /api/gemini/text
        传入 prompt 返回 Gemini 生成的文本
        """
        data = request.json
        prompt = data.get("prompt", "")
        if not prompt:
            return {"error": "No prompt provided."}, 400


        modified_prompt = f"{prompt}"
        
        # 调用 service
        response_text = generate_text(modified_prompt)
        return {"response": response_text}, 200


@api.route("/image")
class GeminiImageResource(Resource):
    @api.expect(image_model)
    def post(self):
        """
        POST /api/gemini/image
        传入 prompt,返回生成图像文件路径
        """
        data = request.json
        prompt = data.get("prompt", "")
        if not prompt:
            return {"error": "No prompt provided."}, 400

        # 调用 service
        file_path = generate_image(prompt)
        return {"image_path": file_path}, 200
