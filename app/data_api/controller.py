import uuid
import datetime
from flask_restx import Namespace, Resource
from flask import request
import http.client
import json

from .model import FinancialReport, StockPrice
from .service import get_financial_data, get_stock_price

api = Namespace("finance")

@api.route("/reports")
class FinancialReportsList(Resource):
    def get(self):
        """Get all financial reports"""
        reports = FinancialReport.objects()
        return [report.to_dict() for report in reports]
    
    def post(self):
        """Create a new financial report"""
        data = request.json
        ticker = data.get("ticker")
        
        if not ticker:
            return {"error": "Ticker symbol is required"}, 400
            
        # Try to get financial data from service
        financial_data = get_financial_data(ticker)
        
        if not financial_data or "error" in financial_data:
            return {"error": "Could not retrieve financial data"}, 400
            
        report = FinancialReport(
            report_id=uuid.uuid4(),
            ticker=ticker,
            company_name=financial_data.get("company_name", ticker),
            data=financial_data,
            last_updated=datetime.datetime.utcnow()
        )
        report.save()
        return report.to_dict(), 201


@api.route("/reports/<string:report_id>")
class FinancialReportResource(Resource):
    def get(self, report_id):
        """Get a specific financial report"""
        report = FinancialReport.objects(report_id=report_id).first()
        if not report:
            return {"error": "Financial report not found"}, 404
        return report.to_dict()
    
    def delete(self, report_id):
        """Delete a financial report"""
        report = FinancialReport.objects(report_id=report_id).first()
        if not report:
            return {"error": "Financial report not found"}, 404
        report.delete()
        return {"message": "Financial report deleted successfully"}, 200


@api.route("/reports/ticker/<string:ticker>")
class FinancialReportByTicker(Resource):
    def get(self, ticker):
        """Get financial report by ticker symbol"""
        report = FinancialReport.objects(ticker=ticker).first()
        
        # If no existing report is found or report is outdated, fetch new data
        if not report or (datetime.datetime.utcnow() - report.last_updated).days > 1:
            financial_data = get_financial_data(ticker)
            
            if not financial_data or "error" in financial_data:
                return {"error": "Could not retrieve financial data"}, 400
                
            if report:
                # Update existing report
                report.data = financial_data
                report.last_updated = datetime.datetime.utcnow()
                report.save()
            else:
                # Create new report
                report = FinancialReport(
                    report_id=uuid.uuid4(),
                    ticker=ticker,
                    company_name=financial_data.get("company_name", ticker),
                    data=financial_data,
                    last_updated=datetime.datetime.utcnow()
                )
                report.save()
                
        return report.to_dict()


@api.route("/prices")
class StockPricesList(Resource):
    def get(self):
        """Get all stock prices"""
        prices = StockPrice.objects()
        return [price.to_dict() for price in prices]
    
    def post(self):
        """Create a new stock price entry"""
        data = request.json
        ticker = data.get("ticker")
        
        if not ticker:
            return {"error": "Ticker symbol is required"}, 400
            
        # Try to get stock price data from service
        price_data = get_stock_price(ticker)
        
        if not price_data or "error" in price_data:
            return {"error": "Could not retrieve stock price data"}, 400
            
        price = StockPrice(
            price_id=uuid.uuid4(),
            ticker=ticker,
            company_name=price_data.get("company_name", ticker),
            price=price_data.get("price"),
            change=price_data.get("change"),
            change_percent=price_data.get("change_percent"),
            volume=price_data.get("volume"),
            timestamp=datetime.datetime.utcnow()
        )
        price.save()
        return price.to_dict(), 201


@api.route("/prices/<string:price_id>")
class StockPriceResource(Resource):
    def get(self, price_id):
        """Get a specific stock price entry"""
        price = StockPrice.objects(price_id=price_id).first()
        if not price:
            return {"error": "Stock price not found"}, 404
        return price.to_dict()


@api.route("/prices/ticker/<string:ticker>")
class StockPriceByTicker(Resource):
    def get(self, ticker):
        """Get latest stock price by ticker symbol"""
        # First check for existing price data
        price = StockPrice.objects(ticker=ticker).order_by('-timestamp').first()
        
        # If no existing price is found or price is outdated (over 1 hour old), fetch new data
        if not price or (datetime.datetime.utcnow() - price.timestamp).total_seconds() > 3600:
            price_data = get_stock_price(ticker)
            
            if not price_data or "error" in price_data:
                return {"error": "Could not retrieve stock price data"}, 400
                
            # Create new price entry
            price = StockPrice(
                price_id=uuid.uuid4(),
                ticker=ticker,
                company_name=price_data.get("company_name", ticker),
                price=price_data.get("price"),
                change=price_data.get("change"),
                change_percent=price_data.get("change_percent"),
                volume=price_data.get("volume"),
                timestamp=datetime.datetime.utcnow()
            )
            price.save()
                
        return price.to_dict()