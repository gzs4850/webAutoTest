#encoding = utf-8
# from util.ObjectMap import *
# from util.KeyBoardUtil import KeyBoardKeys
# from util.ClipboardUtil import Clipboard
# from util.WaitUtil import WaitUtil
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time

from action.PageAction import *

def TestSendMailWithAttachment():

    print("启动浏览器成功")
    open_browser("chrome")
    maximize_browser()
    print("访问126邮箱登录页。。。")
    visit_url("http://mail.126.com")
    sleep(5)

    assert_title(u"126网易免费邮--你的专业电子邮局")
    print(u"访问126邮箱登录页成功")

    waitFrameToBeAvailableAndSwitchToIt("id","x-URS-iframe")
    print(u"输入登录用户名")
    input_string("xpath","//input[@name='email']","123456")
    print(u"输入登录密码")
    input_string("xpath","//input[@name='password']","123456789")
    print(u"登录。。。")
    click("id","dologin")
    sleep(5)
    assert_title(u"网易邮箱")
    print(u"登录成功")

    waitVisibilityOfElementLocated("xpath","//span[text() = '写信']")
    click("xpath","//span[text() = '写信']")
    print(u"开始写信")
    print(u"输入收件人地址")
    input_string("xpath","//div[contains(@id,'_main_emailinput')]/input","liuzhiguo@chalco-steering.com")
    print(u"输入邮件主题")
    input_string("xpath","//div[@aria-label = '邮件主题输入框，请输入邮件主题']/input",u"新邮件")
    print(u"单击上传附件按钮")
    click("xpath","//div[contains(@title,'600首MP3')]")
    sleep(3)
    paste_string(u"e:\\a.txt")
    press_enter_key()
    waitFrameToBeAvailableAndSwitchToIt("xpath","//iframe[@tabindex=1]")
    print(u"写入邮件正文")
    input_string("xpath","/html/body",u"发送一封邮件")
    switch_to_default_content()
    print(u"写信完成")
    print(u"开始发送邮件。。。")
    click("xpath","//header//span[text()='发送']")
    time.sleep(3)
    assert_string_in_pagesource(u"发送成功")
    print(u"邮件发送成功")
    close_browser()


if __name__ == '__main__':
    TestSendMailWithAttachment()