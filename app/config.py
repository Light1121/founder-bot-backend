import os
from flask import Config
from dotenv import load_dotenv


class Config(Config):
    load_dotenv()
    ENABLE_UTC = True
    APP_NAME = "founder-bot"
    #official one please name the database to  "mongo_chatbot"
    # dont use localhost
    # MONGODB_HOST = "127.0.0.1"
    # MONGODB_PORT = 27018
    # MONGODB_SETTINGS = "mongodb+srv://light1121lin:M0SspZexBtSacqMa@cluster0.o6c3pg1.mongodb.net/founderbot-api?retryWrites=true&w=majority&appName=Cluster0"
    # MONGODB_DB = "founderbot-api"
    # MONGODB_USERNAME = "ROOTchatbot"
    # MONGODB_PASSWORD = "ROOTchatbot"
    # MONGODB_AUTHENTICATION_SOURCE = "admin"
    MONGODB_SETTINGS = {
        "db": "founder-bot",
        "host": "mongodb+srv://ROOTchatbot:ROOTchatbot@cluster0.o6c3pg1.mongodb.net/founder-bot?retryWrites=true&w=majority&appName=Cluster0",
        "username": "ROOTchatbot",
        "password": "ROOTchatbot",
        "authentication_source": "admin"
    }


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