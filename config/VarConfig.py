#encoding=utf-8
import os
ieDriverFilePath = "e:\geckodriver.exe"
chromeDriverFilePath = "e:\chromedriver.exe"
firefoxDriverFilePath = "e:\geckodriver.exe"

parentDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
screenPicturesDir = parentDirPath + "\\exceptionpictures\\"
# print(parentDirPath)
# print(screenPicturesDir)

dataFilePath = parentDirPath + u"\\testData\\126邮箱发送邮件.xlsx"

#测试用例表
testCase_testCaseName = 2
testCase_testStepSheetName = 4
testCase_isExecute = 5
testCase_runTime = 6
testCase_testResult = 7

#测试步骤表
testStep_testStepDescribe = 2
testStep_keyWords = 3
testStep_locationType = 4
testStep_locatorExpression = 5
testStep_operateValue = 6
testStep_runTime = 7
testStep_testResult = 8
testStep_errorInfo = 9
testStep_errorPic = 10

