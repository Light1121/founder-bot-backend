SUGGESTION_TEMPLATE  = """
Generate 4 constructive suggestions (one sentence each) for the user to choose from, based on each of the following user messages: 
---- 
User message: 
{message}
---- 
Please list them by serial number 1. 2. 3. 4.
"""

RESPONSE_SUGGESTION_TEMPLATE = """
Based on the AI's response to the user, generate 4 follow-up questions or comments (one sentence each) that the user could use to continue the conversation:
---- 
AI response: 
{response}
---- 
Please list them by serial number 1. 2. 3. 4.
"""