import uuid
import datetime
from flask_restx import Namespace, Resource
from flask import request
from flask import Response, stream_with_context

from .model import Conversation as ConversationModel, Message as MessageModel

api = Namespace("conversations")

@api.route("/")
class ConversationsList(Resource):
    def get(self): # when user lick chat bot
        conversations = ConversationModel.objects()
        result = [conversation.to_dict() for conversation in conversations]
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
        return {"messages": [m.to_dict() for m in conversation.messages]}

    def post(self, conversation_id):
        conversation = ConversationModel.objects(conversation_id=conversation_id).first()
        if not conversation:
            return {"error": "Conversation not found"}, 404

        data = request.json
        ai_mode = data.get("mode", "general_chat")
        user_message = MessageModel(
            message_id=str(uuid.uuid4()),
            role=data.get("role"),
            content=data.get("content"),
            mode=ai_mode,
            file_url=data.get("file_url"),
            image_url=data.get("image_url"),
            timestamp=datetime.datetime.utcnow()
        )
        conversation.messages.append(user_message)
        conversation.save()

        # 对user text message触发 AI 回复
        if data.get("role") == "user" and data.get("content"):
            user_input = data["content"]

            # different mode if AI
            if ai_mode == "suggestion":
                from ..bots.suggestion.service import get_suggestions
                suggestions = get_suggestions(user_input)
                # 构造一个拼接好的回复字符串
                ai_content = "\n".join(f"{i+1}. {s}" for i, s in enumerate(suggestions))
            elif ai_mode == "startup_guide":
                from ..bots.startup_guide.service import plan_startup
                ai_content = plan_startup(user_input)
            elif ai_mode == "draft_assistant":
                from ..bots.draft_assistant.service import draft_doc
                ai_content = draft_doc(user_input)
            elif ai_mode == "trends_analyst":
                from ..bots.trends_analyst.service import analyze_trends
                ai_content = analyze_trends(user_input)
            elif ai_mode == "network_connect":
                from ..bots.network_connect.service import build_network
                ai_content = build_network(user_input)
            elif ai_mode == "insight_engine":
                from ..bots.insight_engine.service import generate_insight
                ai_content = generate_insight(user_input)
            else:
                # default to general chat
                from ..bots.general_chat.service import chat_general
                ai_content = chat_general(user_input)

            ai_message = MessageModel(
                message_id=str(uuid.uuid4()),
                role="assistant",
                content=ai_content,
                mode=ai_mode,
                timestamp=datetime.datetime.utcnow()
            )
            conversation.messages.append(ai_message)
            conversation.save()

            return {
                "user_message": user_message.to_dict(),
                "ai_message": ai_message.to_dict()
            }, 201

        # if not user message, save and no AI respond
        return user_message.to_dict(), 201
    
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

@api.route("/<string:conversation_id>/messages/<string:message_id>/suggestions")
class MessageSuggestions(Resource):
    def get(self, conversation_id, message_id):
        conversation = ConversationModel.objects(conversation_id=conversation_id).first()
        if not conversation:
            return {"error": "Conversation not found"}, 404
        
        # Find the target message
        target_message = None
        for message in conversation.messages:
            if message.message_id == message_id:
                target_message = message
                break
                
        if not target_message:
            return {"error": "Message not found"}, 404
            
        # Only generate suggestions for assistant messages
        if target_message.role != "assistant":
            return {"error": "Suggestions can only be generated for assistant messages"}, 400
            
        # Generate suggestions based on AI response
        from ..bots.suggestion.service import get_response_suggestions
        suggestions = get_response_suggestions(target_message.content)
        
        return {
            "message_id": message_id,
            "suggestions": suggestions
        }
    

@api.route("/<string:conversation_id>/messages/stream")
class MessagesStream(Resource):
    def post(self, conversation_id):
        from ..bots.base import generate_text_stream

        user_input = request.json.get("content", "")

        # SSE
        def event_stream():
            # start event
            yield "event: start\ndata: \n\n"

            # only send small part
            for text in generate_text_stream(user_input):
                # 以 SSE 格式推送
                yield f"data: {text}\n\n"

            #done 标记
            yield "event: done\ndata: \n\n"

        # return Response
        return Response(
            stream_with_context(event_stream()),
            mimetype="text/event-stream"
        )