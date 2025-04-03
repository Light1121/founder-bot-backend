import datetime
from flask_restx import Namespace, Resource
from flask import request

from .model import Conversation as ConversationModel

api = Namespace("conversations")

@api.route("/")
class ConversationsList(Resource):
    def get(self): # when user lick chat bot
        return [
        {
            "conversationID": 1,
            "conversationName": "NewsLetterWeb",
        },
        {
            "conversationID": 2,
            "conversationName": "StartupIdea02",
        },
        {
            "conversationID": 3,
            "conversationName": "StartupIdea03",
        }]

@api.route("/dummyConvoID1")
class Conversation(Resource):
    def get(self):  # when user enter specific chat
        return {
            "conversationID": 1,
            "conversationName": "NewsLetterWeb",
            "messages": [
            {
                "messageID": 100,
                "role": "system",
                "content": "Welcome to the NewsLetterWeb conversation!"
            },
            {
                "messageID": 101,
                "role": "user",
                "content": "Hi, I'd like to set up a newsletter website like this.",
                "imageUrl": "https://example.com/image/chart_123.png"
            },
            {
                "messageID": 103,
                "role": "ai",
                "content": "Sure! Who is your target audience?"
            }
            ],
            "timestamp": "2025-03-11T10:00:00Z"
        }

    
    def post(self): # when user start new chat
        request_conversation = request.json
        conversation = ConversationModel()
        conversation.Conversationid = request_conversation['Conversationid']
        conversation.name = request_conversation['name']
        conversation.timestamp = datetime.datetime.utcnow()
        conversation.save()
        print(conversation._data)
        return "OK", 201

    
    def delete(self): # when user remove chat
        return "DELETED", 200
    
@api.route("/<int:conversation_id>/messages")
class Message(Resource):
    def get(self): # when get message
        return {
            "conversationID": 1,
            "messageID": 100,
            "role": "user",
            "content": "I have written some notes, check this out.",
            "fileUrl": "https://example.com/uploads/document_456.txt",
            "timestamp": "2025-03-11T10:06:00Z"
        }



    def post(self): # sent message
        print(request.data)
        return "OK", 201
    
    def delete(self): #delete message ?? need?
        return "DELETED", 200