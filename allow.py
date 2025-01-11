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
        print(f'页面加载失败: {e}')
        await browser.close()
        return

    # 获取复选框元素并点击
    checkbox = await page.querySelector('input[type="checkbox"]')
    if checkbox:
        await checkbox.click()
    else:
        print('复选框未找到')

    # 获取输入框元素并设置值
    input_field = await page.querySelector('.form-control.is-invalid')
    if input_field:
        await input_field.type(登录密码)
    else:
        print('输入框未找到')

    # 获取提交按钮元素并点击
    submit_button = await page.querySelector('button[type="submit"]')
    if submit_button:
        await submit_button.click()
    else:
        print('提交按钮未找到')

    # 访问链接并等待页面加载完成
    try:
        await page.goto(f'{renew_url}/System/SpecialPardon', {'timeout': 60000})  # 增加超时时间到 60 秒
        await page.waitForNavigation({'timeout': 60000})  # 等待页面加载完成
        print("特赦成功")
    except Exception as e:
        print(f'页面加载失败: {e}')

    # 关闭浏览器
    await browser.close()

# 运行主函数
asyncio.run(main())
