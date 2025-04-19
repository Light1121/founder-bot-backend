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
        ai_mode = request_data.get("mode", "chat")
        user_message = MessageModel(
            message_id=str(uuid.uuid4()),
            role=request_data.get("role"),
            content=request_data.get("content"),
            mode = ai_mode,
            file_url=request_data.get("file_url"),
            image_url=request_data.get("image_url"),
            timestamp=datetime.datetime.utcnow()
        )
        
        # save the current input from user
        conversation.messages.append(user_message)
        conversation.save()
        
        # When user sent message and its text, then generate response
        if request_data.get("role") == "user" and request_data.get("content"):
            from bots.service import generate_text 
            user_input = request_data.get("content")
            if ai_mode == "report":
                # For report mode, use the template
                from .format import BUSINESS_PLAN_TEMPLATE
                prompt = f"{BUSINESS_PLAN_TEMPLATE}\n\n User Input: {user_input}"
            else:
                # Regular chat: just send user content
                prompt = user_input

            # Ensure generate_text returns a proper MessageModel instance
            ai_response = generate_text(prompt)
            
            # Create a proper MessageModel for AI response
            ai_message = MessageModel(
                message_id=str(uuid.uuid4()),
                role="assistant",
                content=ai_response if isinstance(ai_response, str) else ai_response.get("content", ""),
                mode=ai_mode,
                timestamp=datetime.datetime.utcnow()
            )
            
            # AI append to convo
            conversation.messages.append(ai_message)
            conversation.save()
            
            # Return user AND AI output
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