import uuid
import datetime
from flask_restx import Namespace, Resource
from flask import request

from .model import Conversation as ConversationModel, Message as MessageModel

api = Namespace("conversations")

@api.route("/")
class ConversationsList(Resource):
    def get(self): # when user lick chat bot
        conversations = ConversationModel.objects()
        result = [conversation.to_dict() for conversation in conversations]
        print(result)
        return result
    
    def post(self):
        request_conversation = request.json
        conversation = ConversationModel()
        conversation.conversation_id = str(uuid.uuid4())
        conversation.conversation_name = request_conversation.get("conversation_name")
        conversation.timestamp = datetime.datetime.utcnow()
        conversation.save()
        return conversation.to_dict(), 201


@api.route("/<string:conversation_id>")
class Conversation(Resource):
    def get(self, conversation_id):
        conversation = ConversationModel.objects(conversation_id=conversation_id).first()
        if not conversation:
            return {"error": "Conversation not found"}, 404
        return conversation.to_dict()

    def delete(self, conversation_id):
        conversation = ConversationModel.objects(conversation_id=conversation_id).first()
        if not conversation:
            return {"error": "Conversation not found"}, 404
        conversation.delete()
        return {"message": "Conversation deleted successfully"}, 200
    
    def put(self, conversation_id):
        conversation = ConversationModel.objects(conversation_id=conversation_id).first()
        if not conversation:
            return {"error": "Conversation not found"}, 404
        
        request_data = request.json
        if "conversation_name" in request_data:
            conversation.conversation_name = request_data["conversation_name"]
        
        conversation.save()
        return conversation.to_dict()
    
@api.route("/<string:conversation_id>/messages")
class Messages(Resource):
    def get(self, conversation_id):
        conversation = ConversationModel.objects(conversation_id=conversation_id).first()
        if not conversation:
            return {"error": "Conversation not found"}, 404
        return {"messages": [message.to_dict() for message in conversation.messages]}
    
    def post(self, conversation_id):
        conversation = ConversationModel.objects(conversation_id=conversation_id).first()
        if not conversation:
            return {"error": "Conversation not found"}, 404
        
        request_data = request.json
        user_message = MessageModel(
            message_id=str(uuid.uuid4()),
            role=request_data.get("role"),
            content=request_data.get("content"),
            file_url=request_data.get("file_url"),
            image_url=request_data.get("image_url"),
            timestamp=datetime.datetime.utcnow()
        )
        
        # save the current input from user
        conversation.messages.append(user_message)
        conversation.save()
        
        # when use sent message and its text, then generate respond
        if request_data.get("role") == "user" and request_data.get("content"):

                from bots.service import generate_text 
                # use bot
                bot_response = generate_text(f"{format},\n\n User Input here: "+str(request_data.get("content")))
                
                # AI respond
                ai_message = MessageModel(
                    message_id=str(uuid.uuid4()),
                    role="gemini",  # 指定角色为 gemini
                    content=bot_response,
                    timestamp=datetime.datetime.utcnow()
                )
                
                # AI append to convo
                conversation.messages.append(ai_message)
                conversation.save()
                
                # return user AND AI output
                return {
                    "user_message": user_message.to_dict(),
                    "ai_message": ai_message.to_dict()
                }, 201
    
@api.route("/<string:conversation_id>/messages/<string:message_id>")
class Message(Resource):
    def get(self, conversation_id, message_id):
        conversation = ConversationModel.objects(conversation_id=conversation_id).first()
        if not conversation:
            return {"error": "Conversation not found"}, 404
        
        for message in conversation.messages:
            if message.message_id == message_id:
                return message.to_dict()
        
        return {"error": "Message not found"}, 404
    
    def delete(self, conversation_id, message_id):
        conversation = ConversationModel.objects(conversation_id=conversation_id).first()
        if not conversation:
            return {"error": "Conversation not found"}, 404
        
        for i, message in enumerate(conversation.messages):
            if message.message_id == message_id:
                conversation.messages.pop(i)
                conversation.save()
                return {"message": "Message deleted successfully"}, 200
        
        return {"error": "Message not found"}, 404