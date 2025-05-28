from flask_restx import Namespace, Resource
from flask import request
# from .service import get_linkedin_profile

from .service import build_network, search_linkedin_profiles

api = Namespace("network_connect")

# @api.route("/profile")
# class LinkedInProfile(Resource):
#     def post(self):
#         data = request.json or {}
#         name = data.get("name", "")
#         company_name = data.get("company_name", "")
#         job_title = data.get("job_title", "")
#         location = data.get("location", "")
#         keywords = data.get("keywords", "")
#         limit = data.get("limit", 5)
#         result = get_linkedin_profile(name, company_name, job_title, location, keywords, limit)
#         return result

#
@api.route("/search")
class NetworkSearch(Resource):
    def post(self):
        data = request.json or {}
        user_input = data.get("content", "")
        
        if not user_input:
            return {"error": "No user input provided"}, 400
        
        result = build_network(user_input)
        return result

@api.route("/profiles")
class LinkedInProfiles(Resource):
    def post(self):
        data = request.json or {}
        keyword = data.get("keyword", "")
        num_results = data.get("limit", 10)
        
        if not keyword:
            return {"error": "Keyword is required"}, 400
        
        result = search_linkedin_profiles(
            keyword=keyword, 
            num_results=num_results
        )
        return result

@api.route("/test")
class NetworkTest(Resource):
    def get(self):
        """
        test interface
        """
        return {"message": "Network Connect API is working with SerpAPI"}
    
    def post(self):
        """
        test search function
        """
        test_result = search_linkedin_profiles("Software Engineer", 5)
        return test_result