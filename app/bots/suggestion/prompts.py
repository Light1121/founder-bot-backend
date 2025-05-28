SUGGESTION_TEMPLATE  = """
Based on the AI's response to the user, generate 4 follow-up questions or comments (one SHORT sentence each) that the user could use to continue the conversation:
It should not be a analysis of revious responds, should be sugestion question. for example some one give you a bussniess plan, one of the suggestion can be "how do I make a MVP for this"
---- 
User message: 
{message}
---- 
Please list them by serial number 1. 2. 3. 4.
"""

RESPONSE_SUGGESTION_TEMPLATE = """
Based on the AI's response to the user, generate 4 follow-up questions or comments (one SHORT sentence each) that the user could use to continue the conversation:
It should not be a analysis of revious responds, should be sugestion question. for example some one give you a bussniess plan, one of the suggestion can be "how do I make a MVP for this"
---- 
AI response: 
{response}
---- 
Please list them by serial number 1. 2. 3. 4.
"""