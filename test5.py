from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime, timedelta

def setup_browser():
    # 设置 Chrome 浏览器选项
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # 最大化浏览器窗口
    options.add_argument('--disable-gpu')  # 禁用GPU加速
    options.add_argument('--no-sandbox')  # 禁用沙箱
    options.add_argument('--disable-software-rasterizer')  # 禁用软件光栅化
    options.add_argument('--disable-dev-shm-usage')  # 解决资源限制问题
    
    # 初始化浏览器
    driver = webdriver.Chrome(options=options)
    
    return driver

def login_126_email(driver, username, password):
    try:
        # 126邮箱登录URL
        login_url = "https://mail.126.com/"
        
        # 打开登录页面
        driver.get(login_url)
        
        # 减少页面加载等待时间
        time.sleep(1)
        
        # 打印当前页面标题，用于调试
        print("当前页面标题:", driver.title)
        
        # 等待并切换到iframe，因为126邮箱的登录表单在iframe中
        try:
            # 等待iframe出现，减少等待时间
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//iframe"))
            )
            print("找到登录iframe")
            # 切换到iframe
            driver.switch_to.frame(iframe)
        except Exception as e:
            print(f"无法找到或切换到iframe: {e}")
            return False
        
        # 尝试多种定位方式找到用户名输入框
        username_field = None
        for locator in [
            (By.NAME, "email"),
            (By.NAME, "username"),
            (By.ID, "idInput"),
            (By.XPATH, "//input[@placeholder='邮箱帐号或手机号码']"),
            (By.XPATH, "//input[@type='text']"),
            (By.CSS_SELECTOR, "input[type='text']")
        ]:
            try:
                # 减少等待时间
                username_field = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(locator)
                )
                if username_field:
                    print(f"找到用户名输入框，使用定位方式: {locator}")
                    break
            except:
                continue
        
        if not username_field:
            print("无法找到用户名输入框")
            # 切换回主文档，打印页面源码的一部分，用于调试
            driver.switch_to.default_content()
            print("页面HTML片段:", driver.page_source[:1000])
            return False
        
        # 输入用户名
        username_field.clear()
        username_field.send_keys(username)
        print(f"已输入用户名: {username}")
        
        # 尝试多种定位方式找到密码输入框
        password_field = None
        for locator in [
            (By.NAME, "password"),
            (By.ID, "pwdInput"),
            (By.XPATH, "//input[@placeholder='输入密码']"),
            (By.XPATH, "//input[@type='password']"),
            (By.CSS_SELECTOR, "input[type='password']")
        ]:
            try:
                # 减少等待时间
                password_field = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(locator)
                )
                if password_field:
                    print(f"找到密码输入框，使用定位方式: {locator}")
                    break
            except:
                continue
        
        if not password_field:
            print("无法找到密码输入框")
            return False
        
        # 输入密码
        password_field.clear()
        password_field.send_keys(password)
        print("已输入密码")
        
        # 尝试多种定位方式找到登录按钮
        login_button = None
        for locator in [
            (By.ID, "loginBtn"),
            (By.XPATH, "//a[@id='loginBtn']"),
            (By.XPATH, "//button[contains(text(), '登录')]"),
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//input[@type='submit']"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.XPATH, "//a[contains(@class, 'login')]"),
            (By.XPATH, "//a[contains(@class, 'submit')]")
        ]:
            try:
                # 减少等待时间
                login_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(locator)
                )
                if login_button:
                    print(f"找到登录按钮，使用定位方式: {locator}")
                    break
            except:
                continue
        
        if not login_button:
            print("无法找到登录按钮")
            return False
        
        # 点击登录按钮
        login_button.click()
        print("已点击登录按钮")
        
        # 切换回主文档
        driver.switch_to.default_content()
        
        # 减少登录完成等待时间
        time.sleep(2)
        
        # 修改登录成功的判断逻辑
        print("当前URL:", driver.current_url)
        print("当前页面标题:", driver.title)
        
        # 检查是否登录成功 - 更宽松的判断条件
        if "mail.126.com" in driver.current_url:
            # 检查是否有登录后才会出现的元素
            try:
                # 尝试查找登录后才会出现的元素，如收件箱链接
                inbox = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '收件箱')]"))
                )
                if inbox:
                    print("登录成功！找到收件箱链接")
                    return True
            except:
                # 即使找不到收件箱，只要URL变化了，也认为登录成功
                if "login" not in driver.current_url.lower():
                    print("登录成功！URL已变化")
                    return True
                else:
                    print("登录可能失败，URL仍包含login")
                    return False
        else:
            print("登录可能失败，URL不包含mail.126.com")
            return False
            
    except Exception as e:
        print(f"登录过程中发生错误: {e}")
        return False

def get_recent_emails(driver, days=1):
    try:
        # 点击收件箱
        inbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '收件箱')]"))
        )
        inbox.click()
        print("已点击收件箱")
        
        # 等待邮件列表加载
        time.sleep(2)
        
        # 获取当前日期
        today = datetime.now()
        yesterday = today - timedelta(days=days)
        
        # 获取邮件列表
        email_list = []
        
        # 尝试多种定位方式找到邮件列表
        emails = None
        for locator in [
            (By.XPATH, "//div[@class='lb-body']//td[@class='g-mn']"),
            (By.XPATH, "//div[@class='lb-body']//tr[@class='lb-body']"),
            (By.XPATH, "//div[@class='lb-body']//div[@class='lb-body']"),
            (By.XPATH, "//div[@class='lb-body']//li"),
            (By.CSS_SELECTOR, ".lb-body .g-mn"),
            (By.CSS_SELECTOR, ".lb-body tr.lb-body"),
            (By.CSS_SELECTOR, ".lb-body div.lb-body"),
            (By.CSS_SELECTOR, ".lb-body li")
        ]:
            try:
                emails = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located(locator)
                )
                if emails:
                    print(f"找到邮件列表，使用定位方式: {locator}")
                    break
            except:
                continue
        
        if not emails:
            print("无法找到邮件列表")
            return []
        
        # 遍历邮件列表，获取最近一天的邮件
        for email in emails:
            try:
                # 获取邮件日期
                date_element = None
                for date_locator in [
                    (By.XPATH, ".//td[@class='lb-date']"),
                    (By.XPATH, ".//span[@class='lb-date']"),
                    (By.XPATH, ".//div[contains(@class, 'date')]"),
                    (By.CSS_SELECTOR, ".lb-date"),
                    (By.CSS_SELECTOR, "[class*='date']")
                ]:
                    try:
                        date_element = email.find_element(*date_locator)
                        if date_element:
                            break
                    except:
                        continue
                
                if not date_element:
                    continue
                
                date_text = date_element.text.strip()
                
                # 解析日期
                email_date = None
                if "今天" in date_text:
                    email_date = today
                elif "昨天" in date_text:
                    email_date = yesterday
                else:
                    try:
                        # 尝试解析具体日期
                        email_date = datetime.strptime(date_text, "%Y-%m-%d")
                    except:
                        continue
                
                # 检查是否在最近一天内
                if email_date and email_date >= yesterday:
                    # 获取邮件标题
                    title_element = None
                    for title_locator in [
                        (By.XPATH, ".//td[@class='lb-subject']"),
                        (By.XPATH, ".//span[@class='lb-subject']"),
                        (By.XPATH, ".//div[contains(@class, 'subject')]"),
                        (By.CSS_SELECTOR, ".lb-subject"),
                        (By.CSS_SELECTOR, "[class*='subject']")
                    ]:
                        try:
                            title_element = email.find_element(*title_locator)
                            if title_element:
                                break
                        except:
                            continue
                    
                    if not title_element:
                        continue
                    
                    title = title_element.text.strip()
                    
                    # 获取发件人
                    sender_element = None
                    for sender_locator in [
                        (By.XPATH, ".//td[@class='lb-sender']"),
                        (By.XPATH, ".//span[@class='lb-sender']"),
                        (By.XPATH, ".//div[contains(@class, 'sender')]"),
                        (By.CSS_SELECTOR, ".lb-sender"),
                        (By.CSS_SELECTOR, "[class*='sender']")
                    ]:
                        try:
                            sender_element = email.find_element(*sender_locator)
                            if sender_element:
                                break
                        except:
                            continue
                    
                    if not sender_element:
                        continue
                    
                    sender = sender_element.text.strip()
                    
                    # 添加到邮件列表
                    email_list.append({
                        'title': title,
                        'sender': sender,
                        'date': date_text
                    })
            except Exception as e:
                print(f"处理邮件时出错: {e}")
                continue
        
        return email_list
        
    except Exception as e:
        print(f"获取邮件列表时出错: {e}")
        return []

def main():
    # 设置浏览器
    driver = setup_browser()
    
    try:
        # 登录信息
        username = "zj1103121"  # 替换为实际的126邮箱用户名
        password = "zzy1103121"  # 替换为实际的126邮箱密码
        
        # 执行登录
        if login_126_email(driver, username, password):
            # 登录成功后获取最近一天的邮件
            recent_emails = get_recent_emails(driver, days=1)
            
            # 打印邮件信息
            print("\n最近一天的邮件:")
            for i, email in enumerate(recent_emails, 1):
                print(f"{i}. 标题: {email['title']}")
                print(f"   发件人: {email['sender']}")
                print(f"   日期: {email['date']}")
                print()
        
        # 等待一段时间以便观察
        time.sleep(3)
        
    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    main()
