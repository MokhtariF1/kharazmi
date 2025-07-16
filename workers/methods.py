from playwright.sync_api import sync_playwright, TimeoutError
import re
from celery import Celery
from pymongo import MongoClient
from bson import ObjectId
from bs4 import BeautifulSoup
import requests
import pyperclip
import time

app = Celery("eitaa", broker="amqp://localhost", backend="rpc://")

client = MongoClient("127.0.0.1:27017")
db = client["eitaa"]
requests_collection = db["requests"]


@app.task
def get_me(document_id):
    with sync_playwright() as p:
        # وصل شدن به مرورگر
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        page.goto("https://web.eitaa.com/")
        page.wait_for_selector(".c-ripple")
        page.locator(".c-ripple").first.click()
        # کلیک روی تنظیمات
        page.locator("div").filter(has_text=re.compile(
            r"^تنظیمات$")).locator("div").click()
        page.locator("button.btn-icon.tgico-edit.rp").click()
        page.wait_for_selector("div.input-field-input")
        forms = page.query_selector_all("div.input-field-input")
        info = []
        # دریافت اطلاعات به ترتیب در حلقه
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
        # آپدیت نتیجه در دیتابیس
        requests_collection.update_one({"_id": ObjectId(document_id)}, {
                                       "$set": {"result": info_json, "status": 200}})
        page.close()
        return info_json


@app.task
def send_message(document_id, text, peer_id_get):
    with sync_playwright() as p:
        # اتصال به مرورگر
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        # رفتن به چت مورد نظر
        page.goto(f"https://web.eitaa.com/#{peer_id_get}")
        page.locator(".input-message-input").first.wait_for()
        # تایپ متن در فیلد پیام
        page.locator(".input-message-input").first.type(text)
        page.locator("div.btn-send-container").wait_for()
        page.locator("div.btn-send-container").click()
        element = None
        try:
            element = page.query_selector_all('[data-mid]')[-1]
        except IndexError:
            page.goto(f"https://web.eitaa.com/#{peer_id_get}")
        # دریافت فیلد های مورد نظر از المنت
        data_mid, timestamp, peer_id = element.get_attribute("data-mid"), element.get_attribute(
            "data-timestamp"), element.get_attribute("data-peer-id")
        # این حلقه به دلیل همون باگ ایتا نوشته شده چون ممکنه ایتا
        #  در اصل پیام رو ارسال کنه ولی فرانت ایتا به باگ بخوره و جوری نشون بده که ما متوجه نشیم پیام ارسال شده و برای جلوگیری
        #  از منتظر موندن برنامه اگر ارسال پیام بیشتر از ۴ ثانیه طول کشید برنامه تشخیص میده پیام در واقعیت ارسال شده و این باگ ایتا هست که نشون نمیده
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
        # کلیک راست روی پیام برای دریافت آیدی پیام
        element.click(button="right")
        message_link = None
        try:
            if str(peer_id).startswith("-"):
                # کلیک روی کپی لینک پیام
                page.locator("div").filter(has_text=re.compile(
                    r"^کپی لینک پیام$")).locator("div").click()
                # خوندن متن کپی شده از کلیپ بورد سیستم
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
            # بروزرسانی خروجی توی دیتابیس
            requests_collection.update_one({"_id": ObjectId(document_id)}, {
                                           "$set": {"result": result, "status": 200}})
            # بستن صفحه مرورگر
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
        # کلیک کردن روی بخش بالایی چت برای بازکردن اطلاعات چت
        page.wait_for_selector('//*[@id="column-center"]/div/div/div[2]')
        print(page.query_selector('//*[@id="column-center"]/div/div/div[2]').inner_html())
        page.query_selector('//*[@id="column-center"]/div/div/div[2]').query_selector("div.chat-info").click()
        # روش ۲: با XPath (اگر CSS جواب نداد)
        # await page.locator('xpath=//div[starts-with(@class, "sidebar-header topbar")]').click()
        try:
            page.wait_for_selector(
                "div.search-super-content-members ul.chatlist")
        except TimeoutError:
            return 500, []
        # اسکرول کردن به پایین ترین حد ممکن در لیست چت های گروه به خاطر اینکه ایتا در حالت عادی ۵۰ چت اول رو نشون میده و برای مشاهده همه چت ها باید اسکرول کرد
        # همچنین برای اینکه بشه راحت و بهترین حالت اسکرول رو پیاده کرد از تیکه کد جاوااسکریپت برای این کار استفاده شده که برای استفاده از کد های جاوااسکریپت در پلی رایت از فانکشن evaluate استفاده میشه
        page.evaluate('''const s = document.querySelector("div.scrollable.scrollable-y.no-parallax")
                      s.scrollTop = s.scrollHeight
                      ''')
        time.sleep(3)
        members = page.locator(
            "div.search-super-content-members ul.chatlist li.chatlist-chat")
        members_list = []
        # در آخر حلقه میزنیم تا اطلاعات کل ممبر هارو بگیریم
        for i in range(members.count()):
            member = members.nth(i)
            user_peer_id = member.get_attribute("data-peer-id")
            name = member.locator("span.peer-title").text_content()
            user = {
                "peer_id": user_peer_id,
                "name": name,
            }
            members_list.append(user)
        # و آپدیت اطلاعات توی دیتابیس
        requests_collection.update_one({"_id": ObjectId(document_id)}, {
                                       "$set": {"result": members_list, "status": 200, "count": len(members_list)}})
        page.close()
        return 200, members_list


@app.task
def get_chat_info(document_id, peer_id):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        page.goto(f"https://web.eitaa.com/#{peer_id}")
        page.wait_for_selector("div.sidebar-header.topbar")
        # روی بخش بالایی چت برای بازکردن اطلاعاتش کلیک میشه
        page.locator("div.sidebar-header.topbar").click()
        # این اول ترکیب bs4 با پلی رایت در این پروژه هست
        # به دلیل اینکه این بخش با پلی رایت یک سری مشکلات و باگ ها داشت از bs4 برای دریافت اطلاعات چت استفاده کردم
        # که خیلی به شدت سریع تر و بدون باگ تر اطلاعات رو دریافت و خروجی میده
        soup = BeautifulSoup(page.content(), "html.parser")
        # پیدا کردن اسم
        chat_name = soup.find("div", attrs={"class": "profile-name"})
        chat_name = chat_name.text if chat_name.text != " " else None
        # پیدا کردن شماره
        phone = soup.find(
            "div", attrs={"class": "row-title tgico tgico-phone"})
        phone = phone.text if phone.text != " " else None
        # پیدا کردن نام کاربری
        username = soup.find(
            "div", attrs={"class": "row-title tgico tgico-username"})
        username = username.text if username.text != " " else None
        # پیدا کردن بیو کاربر
        bio = soup.find(
            "div", attrs={"class": "row-title tgico tgico-info pre-wrap"})
        print(bio)
        bio = bio.text if bio.text != " " else None
        # اگر هر کدوم از اطلاعات رو کاربر نداشته باشه None خروجی داده میشه
        # و در نهایت خروجی دادن و آپدیت اطلاعات در دیتابیس
        response = {
            "status": 200,
            "username": username,
            "phone": phone,
            "name": chat_name,
            "bio": bio,
        }
        requests_collection.update_one({"_id": ObjectId(document_id)}, {
                                       "$set": {"result": response, "status": 200}})
        page.close()
        return response


@app.task
def change_account_info(first_name=None, last_name=None, bio=None):
    with sync_playwright() as p:
        # وصل شدن به مرورگر
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        page.goto("https://web.eitaa.com/")
        page.wait_for_selector(".c-ripple")
        page.locator(".c-ripple").first.click()
        # کلیک روی تنظیمات
        page.locator("div").filter(has_text=re.compile(
            r"^تنظیمات$")).locator("div").click()
        page.locator("button.btn-icon.tgico-edit.rp").click()
        page.wait_for_selector("div.input-field-input")
        forms = page.query_selector_all("div.input-field-input")
        # بروزرسانی اطلاعات وارد شده پروفایل
        for index, form in enumerate(forms):
            if first_name != None and index == 0:
                form.fill(first_name)
            if last_name != None and index == 1:
                form.fill(last_name)
            if bio != None and index == 2:
                form.fill(bio)
        # کلیک روی ذخیره اطلاعات
        page.locator(
            "button.btn-circle btn-corner z-depth-1 tgico-check rp is-visible".replace(" ", ".")).click()
        response = {"status": 200,
            "message": "Account info updated successfully"}
        page.close()
        return response
