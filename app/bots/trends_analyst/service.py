import os
import requests
from ..base import generate_text
from .prompts import TRENDS_ANALYST

def search_finance_data(keyword: str, data_type: str = "stocks"):
    """
    search google finance data using SerpAPI
    
    Args:
        keyword: search keyword (e.g. "semiconductor", "NVDA", "tech stocks")
        data_type: data type ("stocks", "news", "markets")
    """
    url = "https://serpapi.com/search"
    
    # build different search queries based on data type
    if data_type == "stocks":
        search_query = f"{keyword} stocks finance"
    elif data_type == "news":
        search_query = f"{keyword} finance news"
    elif data_type == "markets":
        search_query = f"{keyword} market trends"
    else:
        search_query = f"{keyword} finance"
    
    params = {
        "engine": "google_finance",
        "q": keyword,
        "api_key": os.getenv("SERPAPI_KEY", "792852410b03385372e9c54eb810a0436ca33a9ce62bf4f55834cb9be34847ca"),
        "hl": "en"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # extract financial data
        finance_results = {
            "keyword": keyword,
            "search_query": search_query,
            "stocks": [],
            "markets": [],
            "news": [],
            "summary": {}
        }
        
        # extract stock data
        if "stocks" in data:
            for stock in data["stocks"]:
                stock_info = {
                    "symbol": stock.get("stock", ""),
                    "name": stock.get("name", ""),
                    "price": stock.get("price", ""),
                    "change": stock.get("change", ""),
                    "change_percent": stock.get("change_percent", ""),
                    "market": stock.get("market", ""),
                    "link": stock.get("link", "")
                }
                finance_results["stocks"].append(stock_info)
        
        # extract market data
        if "markets" in data:
            for market in data["markets"]:
                market_info = {
                    "name": market.get("name", ""),
                    "value": market.get("value", ""),
                    "change": market.get("change", ""),
                    "change_percent": market.get("change_percent", "")
                }
                finance_results["markets"].append(market_info)
        
        # extract news data
        if "news" in data:
            for news_item in data["news"]:
                news_info = {
                    "title": news_item.get("title", ""),
                    "source": news_item.get("source", ""),
                    "time": news_item.get("time", ""),
                    "link": news_item.get("link", ""),
                    "snippet": news_item.get("snippet", "")
                }
                finance_results["news"].append(news_info)
        
        # add search summary
        finance_results["summary"] = {
            "total_stocks": len(finance_results["stocks"]),
            "total_markets": len(finance_results["markets"]),
            "total_news": len(finance_results["news"]),
            "search_keyword": keyword
        }
        
        return finance_results
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"API request failed: {str(e)}",
            "keyword": keyword,
            "stocks": [],
            "markets": [],
            "news": []
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "keyword": keyword,
            "stocks": [],
            "markets": [],
            "news": []
        }


def search_specific_stocks(keyword: str, num_results: int = 10):
    """
    search specific stocks or industry stocks information
    """
    url = "https://serpapi.com/search"
    
    params = {
        "engine": "google",
        "q": f"site:finance.google.com {keyword} stock",
        "api_key": os.getenv("SERPAPI_KEY", "792852410b03385372e9c54eb810a0436ca33a9ce62bf4f55834cb9be34847ca"),
        "num": num_results,
        "hl": "en",
        "gl": "us"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        stocks_info = []
        if "organic_results" in data:
            for result in data["organic_results"]:
                if "finance.google.com" in result.get("link", ""):
                    stock_info = {
                        "title": result.get("title", ""),
                        "link": result.get("link", ""),
                        "snippet": result.get("snippet", ""),
                        "displayed_link": result.get("displayed_link", "")
                    }
                    stocks_info.append(stock_info)
        
        return {
            "keyword": keyword,
            "total_results": len(stocks_info),
            "stocks": stocks_info,
            "search_query": f"site:finance.google.com {keyword} stock"
        }
        
    except Exception as e:
        return {
            "error": f"Stock search failed: {str(e)}",
            "keyword": keyword,
            "stocks": []
        }


def get_market_trends(sector: str):
    """
    get market trends for a specific sector
    """
    url = "https://serpapi.com/search"
    
    params = {
        "engine": "google_finance_markets",
        "trend": "INDEXES",  # 或 "MOST_ACTIVE", "GAINERS", "LOSERS"
        "api_key": os.getenv("SERPAPI_KEY", "792852410b03385372e9c54eb810a0436ca33a9ce62bf4f55834cb9be34847ca"),
        "hl": "en"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            "sector": sector,
            "market_data": data,
            "timestamp": data.get("search_metadata", {}).get("created_at", "")
        }
        
    except Exception as e:
        return {
            "error": f"Market trends search failed: {str(e)}",
            "sector": sector,
            "market_data": {}
        }


def analyze_trends(user_input: str):
    """
    main function: extract keyword from user input and analyze trends
    """
    # 1. use AI to extract keyword
    prompt = TRENDS_ANALYST.format(user_input=user_input)
    raw_keyword = generate_text(prompt).strip()
    keyword = raw_keyword.strip('"').strip()
    
    print(f"User input: {user_input}")
    print(f"Extracted keyword: {keyword}")
    
    # 2. search finance data using keyword
    finance_data = search_finance_data(keyword=keyword)
    
    # 3. if it is a sector keyword, also search related stocks
    if any(sector in keyword.lower() for sector in ['semiconductor', 'tech', 'finance', 'healthcare', 'energy', 'automotive']):
        stock_data = search_specific_stocks(keyword=keyword, num_results=10)
        finance_data["related_stocks"] = stock_data.get("stocks", [])
    
    return finance_data
