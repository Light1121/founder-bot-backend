from flask_mongoengine import Document
from mongoengine.fields import StringField, IntField,DateTimeField

class Conversation(Document):
    Conversationid = IntField()
    name = StringField()
    timestamp = DateTimeField()

class Message(Document):
    Conversationid = IntField()
    MessageID = IntField()
    role = StringField()
    content = StringField()
    file_url = StringField()