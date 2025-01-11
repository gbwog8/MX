import asyncio
from pyppeteer import launch
from datetime import datetime, timedelta
import aiofiles
import random
import requests
import os

# 初始化
# 从环境变量中获取 RENEW_URL 和 PASSWORD
RENEW_URL = os.getenv('RENEW_URL')
PASSWORD = os.getenv('PASSWORD')

renew_url = RENEW_URL  # 格式：https://www.example.com 请注意，后面不带/
登录密码 = PASSWORD


# 全局浏览器实例
browser = None

async def delay_time(ms):
    await asyncio.sleep(ms / 1000)

async def login(renew_url, 登录密码):
    global browser

    page = None  # 确保 page 在任何情况下都被定义
    try:
        if not browser:
            browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])

        page = await browser.newPage()
        await page.goto(renew_url)

        # 获取复选框元素
        checkbox = await page.querySelector('input[type="checkbox"]')
        if checkbox:
            await checkbox.click()
        else:
            print('复选框未找到')

        # 获取输入框元素
        input_field = await page.querySelector('.form-control.is-invalid')
        if input_field:
            await input_field.type(登录密码)
        else:
            print('输入框未找到')

        # 获取提交按钮元素
        submit_button = await page.querySelector('button[type="submit"]')
        if submit_button:
            await submit_button.click()
        else:
            print('提交按钮未找到')

        # 访问链接
        # await page.goto(f'{renew_url}/System/SpecialPardon')
        page = await browser.newPage()
        await page.goto(f'{renew_url}/System/SpecialPardon')



    except Exception as e:
        print(f'登录时出现错误: {e}')
        return False

    finally:
        if page:
            await page.close()

    return True

# 显式的浏览器关闭函数
async def shutdown_browser():
    global browser
    if browser:
        await browser.close()
        browser = None

async def main():
    is_logged_in = await login(renew_url, 登录密码)
    if is_logged_in:
        print("登录成功！")
    else:
        print("登录失败，请检查账号和密码是否正确。")

    # 退出时关闭浏览器
    await shutdown_browser()

if __name__ == '__main__':
    asyncio.run(main())
