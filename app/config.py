from flask import Config

class Config(Config):
    ENABLE_UTC = True
    APP_NAME = "founder-bot"
    MONGODB_HOST = "127.0.0.1"
    MONGODB_PORT = 27017
    MONGODB_DB = "founderbot-api"
    MONGODB_USERNAME = "ROOTchatbot"
    MONGODB_PASSWORD = "ROOTchatbot"

# import os

# class Config:
#     ENABLE_UTC = True
#     APP_NAME = "founder-bot"
    
#     MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27018/founderbot-api")

# import os

# class Config:
#     ENABLE_UTC = True
#     APP_NAME = "founder-bot"
    
#     MONGODB_URI = os.getenv(
#         "MONGODB_URI", 
#         "mongodb://ROOTchatbot:ROOTchatbot@mongo_chatbot:27017/founderbot-api?authSource=admin"
#     )