from playwright.sync_api import sync_playwright

# 初始化
renew_url = ""  # 格式：https://www.example.com 请注意，后面不带/
登录密码 = ''

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # 打开目标网页
    page.goto(renew_url)

    # 获取复选框元素并点击
    checkbox = page.query_selector('input[type="checkbox"]')
    if checkbox:
        checkbox.click()
    else:
        print('复选框未找到')

    # 获取输入框元素并设置值
    input_field = page.query_selector('.form-control.is-invalid')
    if input_field:
        input_field.fill(登录密码)
    else:
        print('输入框未找到')

    # 获取提交按钮元素并点击
    submit_button = page.query_selector('button[type="submit"]')
    if submit_button:
        submit_button.click()
    else:
        print('提交按钮未找到')

    # 访问链接
    page.goto(f'{renew_url}/System/SpecialPardon')

    # 关闭浏览器
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
