from flask import Config
from dotenv import load_dotenv

class Config(Config):
    ENABLE_UTC = True
    APP_NAME = "founder-bot"
    #official one please name the database to  "mongo_chatbot"
    # use dont use localhost
    MONGODB_HOST = "127.0.0.1"
    MONGODB_PORT = 27018
    MONGODB_DB = "founderbot-api"
    MONGODB_USERNAME = "ROOTchatbot"
    MONGODB_PASSWORD = "ROOTchatbot"
    MONGODB_AUTHENTICATION_SOURCE = "admin"
    load_dotenv()

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