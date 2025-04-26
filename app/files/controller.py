import uuid
import datetime
from flask_restx import Namespace, Resource
from flask import request

from .model import Document as DocumentModel

api = Namespace("docs")

@api.route("/")
class DocumentsList(Resource):
    def get(self):
        """Get all documents summary"""
        documents = DocumentModel.objects()
        return [doc.to_summary_dict() for doc in documents]

    def post(self):
        """Create a new document"""
        data = request.json
        doc = DocumentModel(
            doc_id=uuid.uuid4(),
            doc_name=data.get("DocName"),
            content=data.get("content", []),
            timestamp=datetime.datetime.utcnow()
        )
        doc.save()
        return doc.to_dict(), 201


@api.route("/<string:doc_id>")
class Document(Resource):
    def get(self, doc_id):
        doc = DocumentModel.objects(doc_id=doc_id).first()
        if not doc:
            return {"error": "Document not found"}, 404
        return doc.to_dict()

    def put(self, doc_id):
        """Update entire document (name + full content list)"""
        doc = DocumentModel.objects(doc_id=doc_id).first()
        if not doc:
            return {"error": "Document not found"}, 404

        data = request.json
        if "DocName" in data:
            doc.doc_name = data["DocName"]
        if "content" in data and isinstance(data["content"], list):
            doc.content = data["content"]
        doc.save()
        return doc.to_dict()

    def delete(self, doc_id):
        doc = DocumentModel.objects(doc_id=doc_id).first()
        if not doc:
            return {"error": "Document not found"}, 404
        doc.delete()
        return {"message": "Document deleted successfully"}, 200


@api.route("/<string:doc_id>/content")
class DocumentContent(Resource):
    def get(self, doc_id):
        """Get document content array"""
        doc = DocumentModel.objects(doc_id=doc_id).first()
        if not doc:
            return {"error": "Document not found"}, 404
        return {"content": doc.content}

    def post(self, doc_id):
        """Append one new content item"""
        doc = DocumentModel.objects(doc_id=doc_id).first()
        if not doc:
            return {"error": "Document not found"}, 404

        item = request.json.get("content")
        if not item or not isinstance(item, dict) or "type" not in item or "data" not in item:
            return {"error": "Invalid content format. Must include 'type' and 'data' fields"}, 400

        doc.content.append(item)
        doc.save()
        return {"message": "Content added successfully", "content": doc.content}, 201