#encoding = utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WaitUtil(object):

    def __init__(self,driver):
        self.locationTypeDict = {
            "xpath":By.XPATH,
            "id":By.ID,
            "name":By.NAME,
            "css_selector": By.CSS_SELECTOR,
            "class_name":By.CLASS_NAME,
            "tag_name":By.TAG_NAME,
            "link_text":By.LINK_TEXT,
            "partial_link_text":By.PARTIAL_LINK_TEXT
        }
        self.driver = driver
        self.wait = WebDriverWait(self.driver,30)

    def presenceOfElementLocated(self,locatorMethod,locatorExpression,*arg):
        '''显示等待页面元素出现在DOM中，但并不一定可见，存在则返回该页面元素对象'''
        try:
            if self.locationTypeDict.get(locatorMethod.lower()) is not None:
                self.wait.until(
                    EC.presence_of_element_located((
                        self.locationTypeDict[locatorMethod.lower()],
                        locatorExpression)))
            else:
                raise TypeError(u"未找到定位方式，请确认定位方法是否书写正确")
        except Exception as e:
            raise e

    def frameToBeAvailableAndSwitchToIt(self,locatorType,locatorExpression,*arg):
        '''检查frame是否存在，存在则切换进frame中'''
        try:
            self.wait.until(
                EC.frame_to_be_available_and_switch_to_it((
                    self.locationTypeDict[locatorType.lower()],
                    locatorExpression)))
        except Exception as e:
            raise e

    def visibilityOfElementLocated(self,locationType,locatorExpression,*args):
        '''显示等待页面元素出现在DOM中，并且可见，存在则返回该页面元素对象'''
        try:
            self.wait.until(
                EC.visibility_of_element_located((
                    self.locationTypeDict[locationType.lower()],
                    locatorExpression
                ))
            )
        except Exception as e:
            raise e


if __name__ == '__main__':
    from selenium import webdriver
    import time
    driver = webdriver.Chrome(executable_path="E:\\chromedriver.exe")
    driver.get("http://mail.126.com")
    time.sleep(5)
    waitUtil = WaitUtil(driver)
    waitUtil.frameToBeAvailableAndSwitchToIt("xpath","//div[@id='loginDiv']/descendant::iframe")
    waitUtil.visibilityOfElementLocated("xpath","//input[@name='email']")
    waitUtil.presenceOfElementLocated("xpath","//input[@name='email']")
    driver.quit()