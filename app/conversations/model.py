import uuid
from flask_mongoengine import Document
from mongoengine.fields import UUIDField, StringField, IntField, DateTimeField, EmbeddedDocumentField, EmbeddedDocument, ListField


class Message(EmbeddedDocument):
    message_id = StringField(required=True)
    role = StringField(required=True)
    content = StringField(required=True)
    file_url = StringField()
    image_url = StringField()
    mode = StringField(choices=('chat', 'report'), default='chat')
    timestamp = DateTimeField(required=True)


    def to_dict(self):
        return {
            "message_id": self.message_id,
            "role": self.role,
            "content": self.content,
            "file_url": self.file_url if self.file_url else None,
            "image_url": self.image_url if self.image_url else None,
            "mode": self.mode,
            "timestamp": self.timestamp.isoformat()
        }

class Conversation(Document):
    conversation_id = UUIDField(required=True, unique=True, default=uuid.uuid4)
    conversation_name = StringField(required=True)
    messages = ListField(EmbeddedDocumentField(Message), default=[])
    timestamp = DateTimeField(required=True)

    meta = {
        'indexes': [
            {'fields': ['conversation_id'], 'unique': True},
            # Removed the unique index on messages.timestamp
        ],
        'collection': 'conversation'
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "conversation_id": str(self.conversation_id),
            "conversation_name": self.conversation_name,
            "messages": [message.to_dict() for message in self.messages],
            "timestamp": str(self.timestamp),
        }