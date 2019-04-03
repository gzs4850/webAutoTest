#encoding=utf-8
import os
ieDriverFilePath = "e:\geckodriver.exe"
chromeDriverFilePath = "e:\chromedriver.exe"
firefoxDriverFilePath = "e:\geckodriver.exe"

parentDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
screenPicturesDir = parentDirPath + "\\exceptionpictures\\"
# print(parentDirPath)
# print(screenPicturesDir)

# dataFilePath = parentDirPath + u"\\testData\\126邮箱发送邮件.xlsx"
dataFilePath = parentDirPath + "\\testData\\126邮箱创建联系人并发送邮件.xlsx"

#测试用例表
testCase_testCaseName = 1
testCase_frameWorkName = 3
testCase_testStepSheetName = 4
testCase_dataSourceSheetName = 5
testCase_isExecute = 6
testCase_runTime = 7
testCase_testResult = 8

#测试步骤表
testStep_testStepDescribe = 1
testStep_keyWords = 2
testStep_locationType = 3
testStep_locatorExpression = 4
testStep_operateValue = 5
testStep_runTime = 6
testStep_testResult = 7
testStep_errorInfo = 8
testStep_errorPic = 9

#数据源表
dataSource_isExecute = 6
dataSource_email = 2
dataSource_runTime = 7
dataSource_result = 8

