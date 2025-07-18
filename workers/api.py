from fastapi import FastAPI, Response
from methods import get_me as get_me_task, send_message as send_message_task, get_chat_members as get_chat_members_task, get_chat_info as get_chat_info_task, change_account_info as change_account_info_task
from pymongo import MongoClient
import json

app = FastAPI()
client = MongoClient("127.0.0.1:27017")
db = client["eitaa"]
requests_collection = db["requests"]


@app.post("/get_me/")
async def get_me():
    document = requests_collection.insert_one({
        "request_type": "get_me",
        "status": 202,
        "result": None,
    })
    request_id = document.inserted_id
    info = get_me_task.delay(str(request_id))
    info = info.get()
    return Response(json.dumps(info))


@app.post("/send_message/")
async def send_message(text: str, peer_id: str):
    document = requests_collection.insert_one({
        "request_type": "send_message",
        "status": 202,
        "result": None,
    })
    request_id = document.inserted_id
    result = send_message_task.delay(str(request_id), text, peer_id)
    result = result.get()
    if result["status"] == 200:
        return Response(json.dumps(result))
    else:
        return Response(json.dumps(result), status_code=500)


@app.post("/get_chat_memebers/")
async def get_chat_members(peer_id: str):
    document = requests_collection.insert_one({
        "request_type": "GetChatMembers",
        "status": 202,
        "result": None,
        "count": None,
    })
    request_id = document.inserted_id
    result = get_chat_members_task.delay(str(request_id), peer_id)
    status, members_list = result.get()
    info = {
        "status": status,
        "count": len(members_list),
        "members": members_list,
    }
    return Response(json.dumps(info), status_code=status)


@app.post("/get_chat_info/")
async def get_chat_info(peer_id):
    document = requests_collection.insert_one({
        "request_type": "GetChatInfo",
        "status": 202,
        "result": None,
    })
    request_id = document.inserted_id
    result = get_chat_info_task.delay(str(request_id), peer_id)
    result = result.get()
    return Response(json.dumps(result), status_code=200)


@app.put("/change_account_info/")
async def change_account_info(first_name: str = None, last_name: str = None, bio: str = None):
    result = change_account_info_task.delay(first_name, last_name, bio)
    result = result.get()
    return Response(json.dumps(result), status_code=200)
