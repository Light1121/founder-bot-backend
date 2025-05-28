TRENDS_ANALYST = """
Please extract the most relevant financial/market keyword from the following user requirement that would be useful for stock market and finance analysis.

The keyword should be:
- A specific company name (e.g., "Apple", "Tesla", "Microsoft")
- A stock symbol (e.g., "AAPL", "TSLA", "NVDA")
- An industry/sector (e.g., "Semiconductor", "Technology", "Healthcare", "Energy")
- A market concept (e.g., "AI stocks", "Electric vehicles", "Renewable energy")
- A financial instrument (e.g., "S&P 500", "NASDAQ", "Bitcoin")

Examples:
- User input: "I want to know the situation of the semiconductor industry" → Output: "Semiconductor"
- User input: "How is the stock price of Tesla" → Output: "Tesla"
- User input: "What are the AI related stocks" → Output: "AI stocks"
- User input: "How is the performance of Apple company recently" → Output: "Apple"
- User input: "I want to see the trend of technology stocks" → Output: "Technology stocks"
- User input: "How is the Bitcoin market" → Output: "Bitcoin"
- User input: "What is the trend of electric vehicles" → Output: "Electric vehicles"

User Requirements:
{user_input}

Output only the most relevant financial/market keyword, nothing else:
"""
