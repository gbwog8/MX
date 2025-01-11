import asyncio
from pyppeteer import launch
from datetime import datetime, timedelta
import aiofiles
import random
import requests
import os

# 从环境变量中获取 RENEW_URL 和 PASSWORD
RENEW_URL = os.getenv('RENEW_URL')
PASSWORD = os.getenv('PASSWORD')

renew_url = RENEW_URL  # 格式：https://www.example.com 请注意，后面不带/
登录密码 = PASSWORD

async def main():
    # 启动浏览器
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()

    # 打开目标网页
    try:
        await page.goto(renew_url, {'timeout': 60000})  # 增加超时时间到 60 秒
    except Exception as e:
        print
