#encoding = utf-8
from selenium.webdriver.support.ui import WebDriverWait

#获取单个元素
def getElement(driver,locationType,locatorExpression):
    try:
        element = WebDriverWait(driver,30).until(lambda x:x.find_element(by=locationType,value=locatorExpression))
        return element
    except Exception as e:
        raise e

#获取多个元素
def getElements(driver,locationType,locatorExpression):
    try:
        elements = WebDriverWait(driver,30).until(lambda x:x.find_elements(by=locationType,value=locatorExpression))
        return elements
    except Exception as e:
        raise e

if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Firefox(executable_path="e:\geckodriver.exe")
    driver.get("http://www.baidu.com")
    searchBox = getElement(driver,"id","kw")
    print(searchBox.tag_name)
    aList = getElements(driver,"tag name","a")
    print(len(aList))
    driver.quit()