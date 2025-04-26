import uuid
from flask_mongoengine import Document
from mongoengine.fields import UUIDField, StringField, DateTimeField, ListField, DictField


class DocumentContent(DictField):
    """
    Content field for storing document content items.
    Each item has a 'type' (text or image) and 'data'.
    """
    pass


class Document(Document):
    doc_id = UUIDField(required=True, unique=True, default=uuid.uuid4)
    doc_name = StringField(required=True)
    content = ListField(DictField(), default=[])
    timestamp = DateTimeField(required=True)

    meta = {
        'indexes': [
            {'fields': ['doc_id'], 'unique': True},
        ],
        'collection': 'document'
    }

    def to_dict(self):
        return {
            "DocID": str(self.doc_id),
            "DocName": self.doc_name,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }
    
    def to_summary_dict(self):
        """
        Return a summary dictionary with only ID, name and timestamp
        for listing purposes
        """
        return {
            "DocID": str(self.doc_id),
            "DocName": self.doc_name,
            "timestamp": self.timestamp.isoformat()
        }