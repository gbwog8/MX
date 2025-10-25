import asyncio
from playwright.async_api import async_playwright
import os
import sys
from urllib.parse import urlparse

# 初始化
RENEW_URL = os.getenv('RENEW_URL')
PASSWORD = os.getenv('PASSWORD')

# 基础校验，避免空变量导致运行时错误
if not RENEW_URL or not PASSWORD:
    missing = []
    if not RENEW_URL:
        missing.append('RENEW_URL')
    if not PASSWORD:
        missing.append('PASSWORD')
    print(f"缺少必要环境变量：{', '.join(missing)}")
    sys.exit(1)

# 解析 RENEW_URL 以获取基础域名
parsed_url = urlparse(RENEW_URL)
# 组合 scheme (https/http) 和 netloc (xxx.com 或 ip:port)
base_renew_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

# 打印解析结果，方便调试
print(f"原始 RENEW_URL: {RENEW_URL}")
print(f"解析后的基础 URL: {base_renew_url}")

async def main():
    async with async_playwright() as p:
        # Docker 内以 root 运行时常需禁用 sandbox，并规避 /dev/shm 限制
        # 添加 ignore_https_errors=True 来忽略 HTTPS 证书错误
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        page.set_default_timeout(30000)

        # 打开目标网页 (使用原始 RENEW_URL 进行登录操作)
        print(f"正在访问登录页: {RENEW_URL}")
        await page.goto(RENEW_URL)

        # 获取复选框元素
        checkbox = await page.query_selector('input[type="checkbox"]')

        # 检查复选框是否存在并点击
        if checkbox:
            await checkbox.click()
            print('复选框已点击')
        else:
            print('复选框未找到')

        # 获取输入框元素
        input_field = await page.query_selector('.form-control.is-invalid')

        # 检查输入框是否存在并设置值
        if input_field:
            await input_field.fill(PASSWORD)
            print('密码已填充')
        else:
            print('输入框未找到')

        # 获取提交按钮元素
        submit_button = await page.query_selector('button[type="submit"]')

        # 检查提交按钮是否存在并点击
        if submit_button:
            await submit_button.click()
            print('提交按钮已点击')
            # 等待导航完成，或者等待一些元素出现，以确保登录成功
            await page.wait_for_load_state('networkidle') # 等待网络空闲
            print('等待登录页面加载完成')
        else:
            print('提交按钮未找到')

        # 访问链接，使用解析后的基础域名
        target_url = f'{base_renew_url}/System/SpecialPardon'
        print(f"即将访问的特殊链接: {target_url}")
        await page.goto(target_url)
        await page.wait_for_load_state('networkidle') # 等待页面加载完成
        print(f"已访问 {target_url}")

        # 这里可以添加一些检查，例如截图或检查页面内容，以确认操作成功
        # await page.screenshot(path='screenshot_special_pardon.png')


        # 关闭浏览器
        await browser.close()
        print("浏览器已关闭")

if __name__ == '__main__':
    asyncio.run(main())
