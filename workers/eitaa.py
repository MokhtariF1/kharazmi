from playwright.async_api import async_playwright
import asyncio
import re
import methods
import aiohttp


# قرار دادن شماره اکاتت ایتا مورد نظر، شروع با ۹۸
phone = "989386083520"
# تعریف متد اصلی برای مدیریت درخواست های جدید
async def management():
    async with async_playwright() as p:
        requests = {"requests": [{"id": 1, "type": "send_joke", "channel_id": "-69878697", "text": "تست ربات ایتا", "sended": False}, {"id": 2, "type": "send_joke", "channel_id": "-69878697", "text": "تست ربات ایتا 2", "sended": False}, {"id": 3,"type": "send_joke", "channel_id": "-69878697", "text": "بردیوار زندگی ام نوشتم ورود ممنوع ، بگایی آمد و گفت بی سوادم", "sended": False}]}
        # بالا آوردن مرورگر مورد نظر برای انجام عملیات
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        # ساخت صفحه جدید در مرورگر
        page = await context.new_page()
        # رفتن به صفحه وب ایتا
        await page.goto("https://web.eitaa.com/")
        # ابتدا ربات شماره تلفن تعیین شده را در فرم وارد میکند
        await page.locator("div").filter(has_text=re.compile(r"^\+98$")).fill(phone)
        # سپس روی دکمه ادامه در صفحه وب ایتا کلیک میکند
        await page.get_by_role("button", name="ادامه").click()
        # در این مرحله کد برای شماره وارد شده ارسال میشود و برنامه از کاربر میخواهد آن کد را وارد کند تا ربات شروع به کار کند
        #  این حلقه بینهایت برای مدیریت خطا ساخته شده است، چون کدی که ایتا برای شماره ارسال میکنه عدد هست و ممکنه کاربر حروف برای ما وارد کنه پس قبل از اینکه اون رو توی فرم در سایت وب ایتا وارد کنیم،
        #  اول درستی اون رو چک میکنیم تا فشار کمتری بیاد و کار کاربر راحت تر بشه
        # حتی ممکنه کاربر بیشتر یا کمتر از ۵ کاراکتر رمز رو وارد کنه، در نتیجه مشخصا کد اشتباه خواهد بود پس این رو هم چک میکنیم
        get_code = None
        is_num = True
        while is_num:
            # چک کردن عدد بودن یا نبودن کد و در صورت عدد نبودن دریافت مجدد کد از کاربر
            try:
                get_code = int(input("کد دریافت شده را وارد کنید: "))
                # حلقه رو تموم میکنیم اگر که کد به صورت عدد وارد شده بود
                if len(str(get_code)) > 5 or len(str(get_code)) < 5:
                    print("کد وارد شده باید پنج رقم باشد! مجدد تلاش کنید!")
                else:
                    break
            except ValueError:
                print("لطفا یک عدد وارد کنید!")
        await page.get_by_role("textbox").fill(str(get_code))
        print("please wait 20 sec...")
        await asyncio.sleep(20)
        while True:
            # چک کردن اینکه آیا درخواستی در مونگو دی بی وجود دارد که انجام نشده باشد یا خیر
            if len(requests["requests"]) == 0:
                print("درخواستی وجود ندارد")
                await asyncio.sleep(2)
            else:
                # هندل کردن درخواست های جدید
                for request in requests["requests"]:
                    if request["type"] == "send_message":
                        # درخواست ارسال پیام با استفاده از متد تعریف شده در فایل methods
                        await page.goto(f"https://web.eitaa.com/#{request['channel_id']}")
                        response = await methods.send_message(page, request)
                        if response == 200:
                            print(f"message with id {request["id"]} posted to eitaa")
                            await asyncio.sleep(5)
                    elif request["type"] == "send_joke":
                        response = await methods.send_joke(page, request["channel_id"])
                        if response == 200:
                            print(f"joke with id {request['id']} posted to eitaa")
                            await asyncio.sleep(10)
                    else:
                        print("no type found! sleep")
                        await asyncio.sleep(2)
asyncio.run(management())