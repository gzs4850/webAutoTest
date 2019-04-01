#encoding = utf-8
# from util.ObjectMap import *
# from util.KeyBoardUtil import KeyBoardKeys
# from util.ClipboardUtil import Clipboard
# from util.WaitUtil import WaitUtil
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time

from action.PageAction import *
from util.ParseExcel import ParseExcel
from config.VarConfig import *
import traceback
from util.Log import *

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

#创建解析Excel对象
excelObj = ParseExcel()
#将Excel数据加载到内存
excelObj.loadWorkBook(dataFilePath)

#测试用例或步骤执行完成后，写入执行结果信息
def writeTestResult(sheetObj,rowNo,colsNo,testResult,errorInfo=None,picPath=None):

    #测试通过结果为绿色，失败为红色
    colorDict = {"pass":"green","faild":"red"}

    #定义数组区分测试用例和测试步骤中的执行时间和测试结果
    colsDict = {
        "testCase":[testCase_runTime,testCase_testResult],
        "testStep":[testStep_runTime,testStep_testResult]
    }

    try:
        #在测试步骤sheet中写入测试时间
        # print("rowNo:%s" %rowNo)
        # print("colsNo:%s" %colsDict[colsNo][0])
        excelObj.writeCellCurrentTime(sheetObj,rowNo=rowNo,colsNo=colsDict[colsNo][0])
        #在测试步骤sheet中写入测试结果
        excelObj.writeCell(sheetObj,content=testResult,rowNo=rowNo,colsNo=colsDict[colsNo][1],style=colorDict[testResult])
        if errorInfo and picPath:
            # 在测试步骤sheet中写入异常信息
            excelObj.writeCell(sheetObj,content=errorInfo,rowNo=rowNo,colsNo=testStep_errorInfo)
            # 在测试步骤sheet中写入异常截图路径
            excelObj.writeCell(sheetObj,content=picPath,rowNo=rowNo,colsNo=testStep_errorPic)
        else:
            # 在测试步骤sheet中清空异常信息
            excelObj.writeCell(sheetObj,content="",rowNo=rowNo,colsNo=testStep_errorInfo)
            # 在测试步骤sheet中清空异常截图单元格
            excelObj.writeCell(sheetObj,content="",rowNo=rowNo,colsNo=testStep_errorPic)
    except Exception as e:
        print("写EXCEL出错，",traceback.print_exc())


def TestSendMailWithAttachment():
    try:
        #根据Excel文件sheet名获取sheet对象
        caseSheet = excelObj.getSheetByName(u"测试用例")
        #获取测试用例sheet中是否执行对象
        isExecuteColumn = excelObj.getColumn(caseSheet,testCase_isExecute)
        #记录执行成功的测试用例个数
        successfulCase = 0
        #记录需要执行的测试用例个数
        requiredCase = 0

        for idx,i in enumerate(isExecuteColumn[1:]):
            if i.value.lower() == "y":
                requiredCase += 1
                #获取“测试用例”sheet中第idx+2行数据
                # print("idx:%s" %idx)
                caseRow = excelObj.getRow(caseSheet,idx + 2)
                #获取第idx+2行的“步骤sheet”单元格内容
                caseStepSheetName = caseRow[testCase_testStepSheetName-1].value
                print("执行测试步骤sheet名：%s" %caseStepSheetName)

                #根据用例步骤名获取步骤sheet对象
                stepSheet = excelObj.getSheetByName(caseStepSheetName)
                #获取步骤sheet中步骤数
                stepNum = excelObj.getRowsNumber(stepSheet)
                # print(stepNum)
                #记录测试用例步骤的成功数
                successfulSteps = 0
                logging.info("开始执行用例" + '"%s"' %caseRow[testCase_testCaseName-1].value)

                for step in range(2,stepNum+1):
                    stepRow = excelObj.getRow(stepSheet,step)
                    keyWord = stepRow[testStep_keyWords - 1].value
                    locationType = stepRow[testStep_locationType - 1].value
                    locatorExpression = stepRow[testStep_locatorExpression - 1].value
                    operateValue = stepRow[testStep_operateValue - 1].value

                    if isinstance(operateValue,int):
                        operateValue = str(operateValue)

                    # print("关键字 %s" %keyWord)
                    # print("定位类型 %s" %locationType)
                    # print("定位表达式 %s" %locatorExpression)
                    # print("操作值 %s" %operateValue)

                    expressionStr = ""

                    if keyWord and operateValue and locationType is None and locatorExpression is None:
                        expressionStr = keyWord.strip() + "('" + operateValue + "')"
                    elif keyWord and operateValue is None and locationType is None and locatorExpression is None:
                        expressionStr = keyWord.strip() + "()"
                    elif keyWord and locationType and operateValue and locatorExpression is None:
                        expressionStr = keyWord.strip() + "('" + locationType.strip() + "','" + operateValue + "')"
                    elif keyWord and locationType and locatorExpression and operateValue:
                        expressionStr = keyWord.strip() + "('" + locationType.strip() + "','" + \
                                        locatorExpression.replace("'",'"').strip() + "','" + operateValue + "')"
                    elif keyWord and locationType and locatorExpression and operateValue is None:
                        expressionStr = keyWord.strip() + "('" + locationType.strip() + "','" + locatorExpression.replace("'",'"').strip() + "')"
                    print(expressionStr)

                    try:
                        eval(expressionStr)
                        excelObj.writeCellCurrentTime(stepSheet,rowNo=step,colsNo=testStep_runTime)
                    except Exception as e:
                        capturePic = capture_screen()
                        errorInfo = traceback.format_exc()

                        # print(step, testStep_runTime)
                        writeTestResult(stepSheet,step,"testStep","faild",errorInfo,capturePic)
                        logging.info("步骤 %s 执行失败，错误信息：%s" %(stepRow[testStep_testStepDescribe -1].value,errorInfo))
                    else:
                        writeTestResult(stepSheet,step,"testStep","pass")
                        successfulSteps += 1
                        logging.info("步骤 %s 执行通过！" %stepRow[testStep_testStepDescribe - 1].value)

                if successfulSteps == stepNum - 1:
                    writeTestResult(caseSheet,idx+2,"testCase","pass")
                    successfulCase += 1
                else:
                    writeTestResult(caseSheet,idx+2,"testCase","faild")

        logging.info("共 %d 条用例，%d 条需要被执行，本次执行通过 %d 条。" %(len(isExecuteColumn) - 1,requiredCase,successfulCase))
    except Exception as e:
        print(traceback.print_exc())


    # print("启动浏览器成功")
    # open_browser("chrome")
    # maximize_browser()
    # print("访问126邮箱登录页。。。")
    # visit_url("http://mail.126.com")
    # sleep(5)
    #
    # assert_title(u"126网易免费邮--你的专业电子邮局")
    # print(u"访问126邮箱登录页成功")
    #
    # waitFrameToBeAvailableAndSwitchToIt("id","x-URS-iframe")
    # print(u"输入登录用户名")
    # input_string("xpath","//input[@name='email']","123456")
    # print(u"输入登录密码")
    # input_string("xpath","//input[@name='password']","123456789")
    # print(u"登录。。。")
    # click("id","dologin")
    # sleep(5)
    # assert_title(u"网易邮箱")
    # print(u"登录成功")
    #
    # waitVisibilityOfElementLocated("xpath","//span[text() = '写信']")
    # click("xpath","//span[text() = '写信']")
    # print(u"开始写信")
    # print(u"输入收件人地址")
    # input_string("xpath","//div[contains(@id,'_main_emailinput')]/input","liuzhiguo@chalco-steering.com")
    # print(u"输入邮件主题")
    # input_string("xpath","//div[@aria-label = '邮件主题输入框，请输入邮件主题']/input",u"新邮件")
    # print(u"单击上传附件按钮")
    # click("xpath","//div[contains(@title,'600首MP3')]")
    # sleep(3)
    # paste_string(u"e:\\a.txt")
    # press_enter_key()
    # waitFrameToBeAvailableAndSwitchToIt("xpath","//iframe[@tabindex=1]")
    # print(u"写入邮件正文")
    # input_string("xpath","/html/body",u"发送一封邮件")
    # switch_to_default_content()
    # print(u"写信完成")
    # print(u"开始发送邮件。。。")
    # click("xpath","//header//span[text()='发送']")
    # time.sleep(3)
    # assert_string_in_pagesource(u"发送成功")
    # print(u"邮件发送成功")
    # close_browser()


if __name__ == '__main__':
    TestSendMailWithAttachment()