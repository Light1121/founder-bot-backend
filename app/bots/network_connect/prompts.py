# NETWORK_CONNECT = """
# Please extract a single, most relevant keyword from the following user requirement that would be useful for LinkedIn search.

# The keyword should be concise and specific, like "AI Engineer", "Product Manager", "Startup Founder", etc.

# therefore just one single keyword
# so I can fill the the_keyword, nothing else, just respond the keyword.
# User Requirements:
# {user_input}

# Output only the keyword, no extra explanation or formatting.
# """

NETWORK_CONNECT = """
Please extract the most relevant professional keyword or job title from the following user requirement that would be useful for LinkedIn professional search.

The keyword should be:
- A specific job title (e.g., "Software Engineer", "Product Manager", "Data Scientist")
- A professional role (e.g., "Startup Founder", "Marketing Director", "UX Designer")
- A skill area (e.g., "Machine Learning Engineer", "Full Stack Developer")
- An industry expertise (e.g., "Fintech Expert", "Healthcare Consultant")

Examples:
- User input: "I want to build an AI chatbot for customer service" → Output: "AI Engineer"
- User input: "Looking for someone to help with product strategy" → Output: "Product Manager"
- User input: "Need a designer for mobile app UI/UX" → Output: "UX Designer"
- User input: "Want to find investors for my startup" → Output: "Venture Capitalist"

User Requirements:
{user_input}

Output only the most relevant professional keyword/title, nothing else:
"""