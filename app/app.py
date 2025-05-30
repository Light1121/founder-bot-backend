from flask import Flask
from flask_restx import Api
from flask_mongoengine import MongoEngine
from .config import Config

from .conversations.controller import api as conversations_api
from .files.controller import api as files_api

from .bots.network_connect.controller import api as network_connect_api
from .bots.trends_analyst.controller import api as trends_analyst_api

app = Flask(Config.APP_NAME)
app.config.from_object(Config)

MongoEngine(app)

api = Api(app, prefix="/api")

api.add_namespace(conversations_api)
api.add_namespace(files_api)
api.add_namespace(network_connect_api)
api.add_namespace(trends_analyst_api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)