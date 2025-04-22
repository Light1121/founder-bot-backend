from flask import Flask
from flask_restx import Api
from flask_mongoengine import MongoEngine

from .conversations.controller import api as conversations_api
from .config import Config

from .bots.controller import api as gemini_api
from .bots.service import list_available_models

app = Flask(Config.APP_NAME)
app.config.from_object(Config)

MongoEngine(app)

api = Api(app, prefix="/api")

api.add_namespace(conversations_api)

api.add_namespace(gemini_api)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    list_available_models()