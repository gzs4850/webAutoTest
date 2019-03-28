#encoding = utf-8
from util.ObjectMap import *
from util.KeyBoardUtil import KeyBoardKeys
from util.ClipboardUtil import Clipboard
from util.WaitUtil import WaitUtil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def TestSendMailWithAttachment():
    driver = webdriver.Chrome(executable_path="E:\\chromedriver.exe")
    driver.maximize_window()
    print("启动浏览器成功")
    print("访问126邮箱登录页。。。")
    driver.get("http://mail.126.com")
    time.sleep(5)
    assert u"126网易免费邮--你的专业电子邮局" in driver.title
    print(u"访问126邮箱登录页成功")

    wait = WaitUtil(driver)
    wait.frame_available_and_switch_to_it("id","x-URS-iframe")
    print(u"输入登录用户名")
    username = getElement(driver,"xpath","//input[@name='email']")
    username.send_keys("123")
    print(u"输入登录密码")
    passwd = getElement(driver,"xpath","//input[@name='password']")
    passwd.send_keys("123")
    print(u"登录。。。")
    passwd.send_keys(Keys.ENTER)
    time.sleep(5)
    assert u"网易邮箱" in driver.title
    print(u"登录成功")

    element = wait.visibility_element_located("xpath","//span[text() = '写信']")
    element.click()
    print(u"写信。。。")
    receiver = getElement(driver,"xpath","//div[@aria-label = '邮件主题输入框，请输入邮件主题']/input")
    receiver.send_keys(u"邮件主题")
    Clipboard.setText(u"e:\\a.txt")
    Clipboard.getText()
    attachment = getElement(driver,"xpath","//div[contains(@title,'600首MP3')]")
    attachment.click()
    time.sleep(3)
    KeyBoardKeys.twoKeys("ctrl","v")
    KeyBoardKeys.oneKey("enter")

    wait.frame_available_and_switch_to_it("xpath","//iframe[@tabindex=1]")
    body = getElement(driver,"xpath","/html/body")
    body.send_keys(u"发送一封邮件")
    driver.switch_to.default_content()
    print(u"写信完成")
    getElement(driver,"xpath","//header//span[text()='发送']").click()
    print(u"开始发送邮件。。。")
    time.sleep(3)
    assert u"发送成功" in driver.page_source
    print(u"邮件发送成功")
    driver.quit()


if __name__ == '__main__':
    TestSendMailWithAttachment()