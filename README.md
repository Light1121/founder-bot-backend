Just run app.py

git clone https://github.com/Light1121/founder-bot-backend.git cd founder-bot-backend docker-compose up -d

测试接口 curl http://localhost:5000/api/conversations

29/03/2025

still dummy data

do this in postman for now
BOT_LOCAL = http://127.0.0.1:5000/
GET conversations list --> {{BOT_LOCAL}}/conversations
GET conversation ID = 1 --> {{BOT_LOCAL}}/conversations/dummyConvoID1
POST create conversation ID = 1 --> {{BOT_LOCAL}}/conversations/dummyConvoID1
DEL create conversation ID = 1 --> {{BOT_LOCAL}}/conversations/dummyConvoID1