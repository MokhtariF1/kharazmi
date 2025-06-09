from enum import member
from playwright.sync_api import sync_playwright, TimeoutError
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


@app.task
def get_me(document_id):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        page.goto("https://web.eitaa.com/")
        page.wait_for_selector(".c-ripple")
        page.locator(".c-ripple").first.click()
        page.locator("div").filter(has_text=re.compile(
            r"^تنظیمات$")).locator("div").click()
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
        requests_collection.update_one({"_id": ObjectId(document_id)}, {
                                       "$set": {"result": info_json, "status": 200}})
        page.close()
        return info_json


@app.task
def send_message(document_id, text, peer_id_get):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        page.goto(f"https://web.eitaa.com/#{peer_id_get}")
        page.locator(".input-message-input").first.wait_for()
        page.locator(".input-message-input").first.type(text)
        page.locator("div.btn-send-container").wait_for()
        page.locator("div.btn-send-container").click()
        element = None
        try:
            element = page.query_selector_all('[data-mid]')[-1]
        except IndexError:
            page.goto(f"https://web.eitaa.com/#{peer_id_get}")
        data_mid, timestamp, peer_id = element.get_attribute("data-mid"), element.get_attribute(
            "data-timestamp"), element.get_attribute("data-peer-id")
        is_sent = False
        before_sent_time = time.time()
        while is_sent != True:
            now_sent_time = time.time()
            if now_sent_time - before_sent_time > 4:
                is_sent = True
                result = {
                    "status": 522,
                    "request_type": "send_message",
                    "peer_id": peer_id,
                    "msg_id": None,
                    "timestamp": timestamp,
                    "data_mid": data_mid,
                }
                page.close()
                return result
            element_class = element.get_attribute("class")
            is_sent = True if "is-sent" in element_class else False
        element.click(button="right")
        message_link = None
        try:
            if str(peer_id).startswith("-"):
                page.locator("div").filter(has_text=re.compile(
                    r"^کپی لینک پیام$")).locator("div").click()
                message_link = pyperclip.paste()
                message_link = message_link.split('/')[-1]
            result = {
                "status": 200,
                "request_type": "send_message",
                "peer_id": peer_id,
                "msg_id": message_link,
                "timestamp": timestamp,
                "data_mid": element.get_attribute("data-mid"),
            }
            requests_collection.update_one({"_id": ObjectId(document_id)}, {
                                           "$set": {"result": result, "status": 200}})
            page.close()
            return result
        except:
            result = {
                "status": 500,
                "request_type": "send_message",
                "peer_id": peer_id,
                "msg_id": None,
                "timestamp": None,
                "data_mid": None,
            }
            requests_collection.update_one({"_id": ObjectId(document_id)}, {
                                           "$set": {"result": result, "status": 500}})
            return result


@app.task
def get_chat_members(document_id, peer_id):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        page.goto(f"https://web.eitaa.com/#{peer_id}")
        page.locator("div.sidebar-header.topbar").click()
        try:
            page.wait_for_selector(
                "div.search-super-content-members ul.chatlist")
        except TimeoutError:
            return 500, []
        page.evaluate('''const s = document.querySelector("div.scrollable.scrollable-y.no-parallax")
                      s.scrollTop = s.scrollHeight
                      ''')
        time.sleep(3)
        members = page.locator(
            "div.search-super-content-members ul.chatlist li.chatlist-chat")
        members_list = []
        for i in range(members.count()):
            member = members.nth(i)
            user_peer_id = member.get_attribute("data-peer-id")
            name = member.locator("span.peer-title").text_content()
            user = {
                "peer_id": user_peer_id,
                "name": name,
            }
            members_list.append(user)
        requests_collection.update_one({"_id": ObjectId(document_id)}, {
                                       "$set": {"result": members_list, "status": 200, "count": len(members_list)}})
        return 200, members_list


# @app.task
# def get_chat_info(document_id, peer_id):