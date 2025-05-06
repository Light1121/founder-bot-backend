import http.client
import json

def get_financial_data(ticker):
    """
    Fetches financial data for a given ticker from Yahoo Finance API
    """
    conn = http.client.HTTPSConnection("yahoo-finance15.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "98c131ec14mshc90d977c13d30cap1217bbjsn6e7fa4734ad5",
        'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com"
    }
    
    try:
        # Get company profile
        conn.request("GET", f"/api/v2/companies/profile/{ticker}", headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            return {"error": f"API returned status {response.status}"}
            
        data = json.loads(response.read().decode("utf-8"))
        
        profile = data.get("profile", {})
        company_name = profile.get("name", ticker.upper())
        
        # Get income statement
        conn.request("GET", f"/api/v2/companies/financial-statements/{ticker}", headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            return {"error": f"API returned status {response.status}"}
            
        financial_data = json.loads(response.read().decode("utf-8"))
        
        # Combine data
        result = {
            "company_name": company_name,
            "profile": profile,
            "financials": financial_data
        }
        
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def get_stock_price(ticker):
    """
    Fetches current stock price data for a given ticker from Yahoo Finance API
    """
    conn = http.client.HTTPSConnection("yahoo-finance15.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "98c131ec14mshc90d977c13d30cap1217bbjsn6e7fa4734ad5",
        'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com"
    }
    
    try:
        conn.request("GET", f"/api/v2/quotes/{ticker}", headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            return {"error": f"API returned status {response.status}"}
            
        data = json.loads(response.read().decode("utf-8"))
        
        quote_data = data.get("data", {})
        if not quote_data:
            return {"error": "No quote data available"}
            
        company_name = quote_data.get("longName", ticker.upper())
        
        return {
            "company_name": company_name,
            "price": quote_data.get("regularMarketPrice"),
            "change": quote_data.get("regularMarketChange"),
            "change_percent": quote_data.get("regularMarketChangePercent"),
            "volume": quote_data.get("regularMarketVolume")
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()