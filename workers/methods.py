from playwright.sync_api import sync_playwright
import re
from celery import Celery
from pymongo import MongoClient
from bson import ObjectId
import pyperclip
import time

app = Celery("eitaa", broker="amqp://localhost", backend="rpc://")

client = MongoClient("127.0.0.1:27017")
db = client["eitaa"]
requests_collection = db["requests"]

# # متد ارسال پیام در ایتا
# async def send_message(page: Page, request: Dict):
#     request_text = request["text"]
#     await page.locator(".input-message-input").first.fill(request_text)
#     # await page.get_by_role("button", name="ارسال").click()
#     await page.locator("div.btn-send-container").click()
#     return 200
# async def send_joke(page: Page, request_channel_id):
#     request_text = None
#     await page.goto(f"https://web.eitaa.com/#{request_channel_id}")
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://api.codebazan.ir/jok/') as response:
#             request_text = await response.text()
#     await page.locator(".input-message-input").first.fill(request_text)
#     # await page.get_by_role("button", name="ارسال").click()
#     await page.locator("div.btn-send-container").click()
#     return 200
@app.task
def get_me(document_id):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]
        page.goto("https://web.eitaa.com/")
        page.wait_for_selector(".c-ripple")
        page.locator(".c-ripple").first.click()
        page.locator("div").filter(has_text=re.compile(r"^تنظیمات$")).locator("div").click()
        page.locator("button.btn-icon.tgico-edit.rp").click()
        page.wait_for_selector("div.input-field-input")
        forms = page.query_selector_all("div.input-field-input")
        info = []
        for form in forms:
            value = form.inner_text()
            info.append(value)
        info_json = {
            "request_type": "get_me",
            "status": 200,
            "first_name": info[0],
            "last_name": info[1],
            "bio": info[2],
        }
        requests_collection.update_one({"_id": ObjectId(document_id)}, {"$set": {"result": info_json, "status": 200}})
        page.goto("https://web.eitaa.com/")
        return info_json
@app.task
def send_message(document_id, text, peer_id_get, reply=None):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        # page.goto("https://web.eitaa.com/")
        # time.sleep(1)
        page.goto(f"https://web.eitaa.com/#{peer_id_get}")
        # time.sleep(1)
        page.locator(".input-message-input").first.wait_for()
        page.locator(".input-message-input").first.fill(text)
        page.locator("div.btn-send-container").wait_for()
        page.locator("div.btn-send-container").click()
        element = None
        try:
            element = page.query_selector_all('[data-mid]')[-1]
        except IndexError:
            page.goto(f"https://web.eitaa.com/#{peer_id}")
        data_mid, timestamp, peer_id = element.get_attribute("data-mid"), element.get_attribute("data-timestamp"), element.get_attribute("data-peer-id")
        print(data_mid)
        is_sent = False
        before_sent_time = time.time()
        while is_sent != True:
            now_sent_time = time.time()
            # print(before_sent_time - now_sent_time)
            if now_sent_time - before_sent_time > 4:
                print("_____is_sent")
                is_sent = True
                result = {
                    "status": 522,
                    "request_type": "send_message",
                    "peer_id": peer_id,
                    "msg_id": None,
                    "timestamp": timestamp,
                    "data_mid": data_mid,
                    "reply": None,
                }
                return result
            element_class = element.get_attribute("class")
            is_sent = True if "is-sent" in element_class else False
        element.click(button="right")
        message_link = None
        try:
            # page.locator("div").filter(has_text=re.compile(r"^کپی لینک پیام$")).locator("div").wait_for()
            if str(peer_id).startswith("-"):
                page.locator("div").filter(has_text=re.compile(r"^کپی لینک پیام$")).locator("div").click()
                message_link = pyperclip.paste()
                message_link = message_link.split('/')[-1]
            result = {
                "status": 200,
                "request_type": "send_message",
                "peer_id": peer_id,
                "msg_id": message_link,
                "timestamp": timestamp,
                "data_mid": element.get_attribute("data-mid"),
                "reply": reply,
            }
            requests_collection.update_one({"_id": ObjectId(document_id)}, {"$set": {"result": result, "status": 200}})
            # context.new_page()
            page.close()
            return result
        except:
            print("error load")
            result = {
                "status": 500,
                "request_type": "send_message",
                "peer_id": peer_id,
                "msg_id": None,
                "timestamp": None,
                "data_mid": None,
                "reply": None,
            }
            requests_collection.update_one({"_id": ObjectId(document_id)}, {"$set": {"result": result, "status": 500}})
            return result