Just run app.py

git clone https://github.com/Light1121/founder-bot-backend.git cd founder-bot-backend docker-compose up -d

测试接口 curl http://localhost:5000/api/conversations

BOT_LOCAL --> http://127.0.0.1:5000//api


13/04/2025

conversation

    GET conversations list --> {{BOT_LOCAL}}/conversations

    POST create conversation --> {{BOT_LOCAL}}/conversations/

        {
            "conversation_name": "1111"
        }

    GET conversation ID -->  {{BOT_LOCAL}}/conversations/{conversation_id}

    DEL delete conversation ID --> {{BOT_LOCAL}}/conversations/{conversation_id}

    PUT Change Convo Name by ID --> {{BOT_LOCAL}}/conversations/{conversation_id}

messages

    GET messsages --> {{BOT_LOCAL}}/conversations/{conversation_id}/messages

    POST send messsage --> {{BOT_LOCAL}}/conversations/{conversation_id}/messages

        {
        "role": "user",
        "content": "Outline a business plan for a photo"
        }

    GET message ID --> {{BOT_LOCAL}}/conversations/{conversation_id}/messages/{messages_id}

    DELETE --> {{BOT_LOCAL}}/conversations/{conversation_id}/messages{messages_id}

BOT

    POST gemini/text --> {{BOT_LOCAL}}/gemini/text