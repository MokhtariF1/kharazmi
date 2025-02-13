from fastapi import FastAPI, Response
from methods import get_me, send_message
from pymongo import MongoClient
import json


app = FastAPI()
client = MongoClient("127.0.0.1:27017")
db = client["eitaa"]
requests_collection = db["requests"]
@app.post("/get-me/")
async def GetMe():
    document = requests_collection.insert_one({
        "request_type": "get_me",
        "status": 202,
        "result": None,
    })
    request_id = document.inserted_id
    info = get_me.delay(str(request_id))
    info = info.get()
    return Response(json.dumps(info))
@app.post("/send-message/")
async def SendMessage(text, peer_id):
    document = requests_collection.insert_one({
        "request_type": "send_message",
        "status": 202,
        "result": None,
    })
    request_id = document.inserted_id
    result = send_message.delay(str(request_id), text, peer_id)
    result = result.get()
    if result["status"] == 200:
        return Response(json.dumps(result))
    else:
        return Response(json.dumps(result), status_code=500)