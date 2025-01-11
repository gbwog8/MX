from selenium import webdriver
from selenium.webdriver.common.by import By

# 初始化
renew_url = "renew链接" #格式：https://www.example.com    请注意，后面不带/
登录密码 = '在此输入登录密码'

# 初始化WebDriver（确保你已经安装了相应的浏览器驱动程序）
driver = webdriver.Chrome()

# 打开目标网页
driver.get(renew_url)

# 获取复选框元素
checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# 检查复选框是否存在并点击
if checkbox:
    checkbox.click()
else:
    print('复选框未找到')

# 获取输入框元素
input_field = driver.find_element(By.CSS_SELECTOR, '.form-control.is-invalid')

# 检查输入框是否存在并设置值
if input_field:
    input_field.send_keys(登录密码)
else:
    print('输入框未找到')

# 获取提交按钮元素
submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

# 检查提交按钮是否存在并点击
if submit_button:
    submit_button.click()
else:
    print('提交按钮未找到')

# 访问链接
driver.get(f'{renew_url}/System/SpecialPardon')

# 关闭浏览器
driver.quit()
