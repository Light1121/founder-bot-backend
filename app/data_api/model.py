import uuid
from flask_mongoengine import Document
from mongoengine.fields import UUIDField, StringField, DateTimeField, DictField, ListField, FloatField


class FinancialReport(Document):
    report_id = UUIDField(required=True, unique=True, default=uuid.uuid4)
    ticker = StringField(required=True)
    company_name = StringField(required=True)
    last_updated = DateTimeField(required=True)
    data = DictField(required=True)
    
    meta = {
        'indexes': [
            {'fields': ['report_id'], 'unique': True},
            {'fields': ['ticker']},
        ],
        'collection': 'financial_reports'
    }
    
    def to_dict(self):
        return {
            "report_id": str(self.report_id),
            "ticker": self.ticker,
            "company_name": self.company_name,
            "data": self.data,
            "last_updated": self.last_updated.isoformat()
        }


class StockPrice(Document):
    price_id = UUIDField(required=True, unique=True, default=uuid.uuid4)
    ticker = StringField(required=True)
    company_name = StringField(required=True)
    timestamp = DateTimeField(required=True)
    price = FloatField(required=True)
    change = FloatField()
    change_percent = FloatField()
    volume = FloatField()
    
    meta = {
        'indexes': [
            {'fields': ['price_id'], 'unique': True},
            {'fields': ['ticker']},
            {'fields': ['timestamp']},
        ],
        'collection': 'stock_prices'
    }
    
    def to_dict(self):
        return {
            "price_id": str(self.price_id),
            "ticker": self.ticker,
            "company_name": self.company_name,
            "price": self.price,
            "change": self.change,
            "change_percent": self.change_percent,
            "volume": self.volume,
            "timestamp": self.timestamp.isoformat()
        }