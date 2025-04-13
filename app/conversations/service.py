# import uuid
# import datetime
# from .model import Conversation as ConversationModel
# from flask  import request


# class ConversationService():
#     def get_all_conversations(self):
#         conversations = ConversationModel.objects()
#         return [conversation.to_dict() for conversation in conversations]

#     def create_conversation(self,name: str):
#         request_conversation = request.json
#         conversation = ConversationModel()
#         conversation.conversation_id = str(uuid.uuid4())
#         conversation.conversation_name = request_conversation.get("conversation_name")
#         conversation.timestamp = datetime.datetime.utcnow()
#         conversation.save()
#         return conversation.to_dict()

#     def get_conversation_by_uuid(self,conv_uuid: str):
#         return ConversationModel.objects(id=ConversationModel.conversation_id)
#     def delete_conversation_by_uuid(conv_uuid: str):
#         conv = ConversationModel.objects(conversation_id=conv_uuid).first()
#         if not conv:
#             return False
#         conv.delete()
#         return True