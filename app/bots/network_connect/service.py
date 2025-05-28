import os
import requests
from ..base import generate_text
from .prompts import NETWORK_CONNECT

# def get_linkedin_profile(keyword: str, page: int = 1):
#     url = "https://fresh-linkedin-profile-data.p.rapidapi.com/google-profiles"
#     payload = {
#         "keyword": keyword,
#         "page":    page
#     }
#     headers = {
#         "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
#         "x-rapidapi-host":"fresh-linkedin-profile-data.p.rapidapi.com",
#         "Content-Type":  "application/json"
#     }
#     resp = requests.post(url, json=payload, headers=headers)
#     return resp.json()

# SerpAPI
def search_linkedin_profiles(keyword: str, num_results: int = 10):

    url = "https://serpapi.com/search"
    
    params = {
        "engine": "google",
        "q": f"site:linkedin.com/in {keyword}",  # search linkedin profiles
        "api_key": os.getenv("SERPAPI_KEY", "792852410b03385372e9c54eb810a0436ca33a9ce62bf4f55834cb9be34847ca"),
        "num": num_results,
        "hl": "en",  # language
        "gl": "us"   # country
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # return search results --> list of profiles
        profiles = []
        if "organic_results" in data:
            for result in data["organic_results"]:
                profile = {
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "displayed_link": result.get("displayed_link", "")
                }
                profiles.append(profile)
        
        return {
            "keyword": keyword,
            "total_results": len(profiles),
            "profiles": profiles,
            "search_query": f"site:linkedin.com/in {keyword}"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"API request failed: {str(e)}",
            "keyword": keyword,
            "profiles": []
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "keyword": keyword,
            "profiles": []
        }


def build_network(user_input: str):
    prompt = NETWORK_CONNECT.format(user_input=user_input)
    raw_keyword = generate_text(prompt).strip()
    keyword = raw_keyword.strip('"').strip()
    
    print(f"User input: {user_input}")
    print(f"Extracted keyword: {keyword}")

    search_results = search_linkedin_profiles(keyword=keyword, num_results=10)
    return search_results