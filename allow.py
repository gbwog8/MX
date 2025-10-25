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
base_renew_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

# 打印解析结果，方便调试
print(f"原始 RENEW_URL: {RENEW_URL}")
print(f"解析后的基础 URL: {base_renew_url}")

async def main():
    MAX_RETRIES = 3
    success = False

    async with async_playwright() as p:
        for attempt in range(MAX_RETRIES):
            print(f"--- [ATTEMPT {attempt + 1}/{MAX_RETRIES}] ---")
            browser = None  # 初始化 browser 变量
            try:
                # 1. 在每次循环中都启动一个全新的浏览器
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--ignore-certificate-errors'  # <-- 强烈建议保持启用以解决 SSL 问题
                    ]
                )
                context = await browser.new_context(ignore_https_errors=True)
                page = await context.new_page()
                page.set_default_timeout(30000)

                # 2. 执行所有核心操作
                print(f"正在访问登录页: {RENEW_URL}")
                await page.goto(RENEW_URL)
                
                print("访问页面后，开始强制等待20秒...")
                await asyncio.sleep(20)
                print("20秒等待结束，继续执行脚本。")
                
                # 查找并操作页面元素
                checkbox = await page.query_selector('input[type="checkbox"]')
                if checkbox:
                    await checkbox.click()
                    print('复选框已点击')
                else:
                    print('复选框未找到')

                input_field = await page.query_selector('.form-control.is-invalid')
                if input_field:
                    await input_field.fill(PASSWORD)
                    print('密码已填充')
                else:
                    print('输入框未找到')

                submit_button = await page.query_selector('button[type="submit"]')
                if submit_button:
                    await submit_button.click()
                    print('提交按钮已点击')
                    await page.wait_for_load_state('networkidle')
                    print('等待登录页面加载完成')
                else:
                    print('提交按钮未找到')

                target_url = f'{base_renew_url}/System/SpecialPardon'
                print(f"即将访问的特殊链接: {target_url}")
                await page.goto(target_url, wait_until='networkidle')
                print(f"已访问 {target_url}")

                # 3. 如果所有操作都成功，设置标志并跳出循环
                print(f"--- [SUCCESS on attempt {attempt + 1}] ---")
                success = True
                break

            except Exception as e:
                # 4. 如果发生任何异常，打印错误信息
                print(f"--- [FAILED on attempt {attempt + 1}] ---")
                print(f"Error: {e}")
                if attempt < MAX_RETRIES - 1:
                    print("将在5秒后重试...")
                    await asyncio.sleep(5)
            
            finally:
                # 5. 无论成功与否，都确保关闭当前浏览器实例
                if browser:
                    await browser.close()
                    print(f"Attempt {attempt + 1} browser closed.")

    # 6. 在所有重试结束后，检查最终是否成功
    if not success:
        print("所有重试均失败，程序将以错误状态退出。")
        sys.exit(1)
    else:
        print("程序成功执行完毕。")


if __name__ == '__main__':
    asyncio.run(main())
