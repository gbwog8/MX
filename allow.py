import asyncio
from playwright.async_api import async_playwright
import os
import sys

# 初始化
RENEW_URL = os.getenv('RENEW_URL')
PASSWORD = os.getenv('PASSWORD')

renew_url = RENEW_URL  # 格式：https://www.example.com 请注意，后面不带/
登录密码 = PASSWORD

# 基础校验，避免空变量导致运行时错误
if not renew_url or not 登录密码:
    missing = []
    if not renew_url:
        missing.append('RENEW_URL')
    if not 登录密码:
        missing.append('PASSWORD')
    print(f"缺少必要环境变量：{', '.join(missing)}")
    sys.exit(1)

async def main():
    async with async_playwright() as p:
        # Docker 内以 root 运行时常需禁用 sandbox，并规避 /dev/shm 限制
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage'  # '--ignore-certificate-errors'  # <--- 添加这一行
            ]
        )
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        page.set_default_timeout(30000)

        # 打开目标网页
        await page.goto(renew_url)

        # 获取复选框元素
        checkbox = await page.query_selector('input[type="checkbox"]')

        # 检查复选框是否存在并点击
        if checkbox:
            await checkbox.click()
        else:
            print('复选框未找到')

        # 获取输入框元素
        input_field = await page.query_selector('.form-control.is-invalid')

        # 检查输入框是否存在并设置值
        if input_field:
            await input_field.fill(登录密码)
        else:
            print('输入框未找到')

        # 获取提交按钮元素
        submit_button = await page.query_selector('button[type="submit"]')

        # 检查提交按钮是否存在并点击
        if submit_button:
            await submit_button.click()
        else:
            print('提交按钮未找到')

        # 访问链接
        await page.goto(f'{renew_url}/System/SpecialPardon')

        # 关闭浏览器
        await browser.close()

asyncio.run(main())
