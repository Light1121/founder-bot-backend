from flask_restx import Namespace, Resource
from flask import request
from .service import analyze_trends, search_finance_data, search_specific_stocks, get_market_trends

api = Namespace("trends_analyst")

@api.route("/analyze")
class TrendsAnalyze(Resource):
    def post(self):
        """
        主要分析接口：从用户描述中提取关键词并分析市场趋势
        """
        data = request.json or {}
        user_input = data.get("content", "")
        
        if not user_input:
            return {"error": "No user input provided"}, 400
        
        result = analyze_trends(user_input)
        return result

@api.route("/finance")
class FinanceData(Resource):
    def post(self):
        """
        直接金融数据搜索接口
        """
        data = request.json or {}
        keyword = data.get("keyword", "")
        data_type = data.get("type", "stocks")  # stocks, news, markets
        
        if not keyword:
            return {"error": "Keyword is required"}, 400
        
        result = search_finance_data(keyword=keyword, data_type=data_type)
        return result

@api.route("/stocks")
class StocksSearch(Resource):
    def post(self):
        """
        股票搜索接口
        """
        data = request.json or {}
        keyword = data.get("keyword", "")
        num_results = data.get("limit", 10)
        
        if not keyword:
            return {"error": "Keyword is required"}, 400
        
        result = search_specific_stocks(keyword=keyword, num_results=num_results)
        return result

@api.route("/markets")
class MarketTrends(Resource):
    def post(self):
        """
        市场趋势接口
        """
        data = request.json or {}
        sector = data.get("sector", "general")
        
        result = get_market_trends(sector=sector)
        return result

@api.route("/test")
class TrendsTest(Resource):
    def get(self):
        """
        测试接口
        """
        return {"message": "Trends Analyst API is working with SerpAPI"}
    
    def post(self):
        """
        测试分析功能
        """
        test_result = search_finance_data("Technology stocks", "stocks")
        return test_result