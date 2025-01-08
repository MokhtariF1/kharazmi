from playwright.async_api import async_playwright, Page
from typing import Dict
import aiohttp
# متد ارسال پیام در ایتا
async def send_message(page: Page, request: Dict):
    request_text = request["text"]
    await page.locator(".input-message-input").first.fill(request_text)
    # await page.get_by_role("button", name="ارسال").click()
    await page.locator("div.btn-send-container").click()
    return 200
async def send_joke(page: Page, request_channel_id):
    request_text = None
    await page.goto(f"https://web.eitaa.com/#{request_channel_id}")
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.codebazan.ir/jok/') as response:
            request_text = await response.text()
    await page.locator(".input-message-input").first.fill(request_text)
    # await page.get_by_role("button", name="ارسال").click()
    await page.locator("div.btn-send-container").click()
    return 200