#encoding = utf-8
from . import *
from .CreateContacts import dataDriverFun
from .WriteTestResult import writeTestResult
from util.Log import *

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

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
            #获取测试用例名称
            caseName = excelObj.getCellOfValue(caseSheet,rowNo=idx+2,colsNo=testCase_testCaseName)

            if i.value.lower() == "y":
                requiredCase += 1
                #获取用例使用的框架
                useFrameWorkName = excelObj.getCellOfValue(caseSheet,rowNo=idx+2,colsNo=testCase_frameWorkName)
                #获取用例对应的步骤sheet名
                stepSheetName = excelObj.getCellOfValue(caseSheet,rowNo=idx+2,colsNo=testCase_testStepSheetName)
                logging.info("---执行测试用例 ‘%s’ ---" %caseName)

                if useFrameWorkName == "数据":
                    logging.info("----------调用数据驱动----------")
                    #获取测试用例表中数据驱动使用的sheet名
                    dataSheetName = excelObj.getCellOfValue(caseSheet,rowNo=idx+2,colsNo=testCase_dataSourceSheetName)
                    #获取idx+2行用例对应的步骤sheet对象
                    stepSheetObj = excelObj.getSheetByName(stepSheetName)
                    #获取idx+2行用例对应的数据sheet对象
                    dataSheetObj = excelObj.getSheetByName(dataSheetName)
                    #执行数据驱动
                    result = dataDriverFun(dataSheetObj,stepSheetObj)
                    if result:
                        logging.info("用例 %s 执行成功" %caseName)
                        successfulCase += 1
                        writeTestResult(caseSheet,rowNo=idx+2,colsNo="testCase",testResult="pass")
                    else:
                        logging.info("用例 %s 执行失败" %caseName)
                        writeTestResult(caseSheet,rowNo=idx+2,colsNo="testCase",testResult="faild")

                elif useFrameWorkName == "关键字":
                    logging.info("----------调用关键字驱动----------")
                    # 获取idx+2行用例对应的步骤sheet对象
                    caseStepObj = excelObj.getSheetByName(stepSheetName)
                    # 获取步骤sheet表中行数
                    stepNums = excelObj.getRowsNumber(caseStepObj)
                    #定义成功步骤条数
                    successfulSteps = 0
                    # logging.info("测试用例共 %s 步" %(stepNums-1))

                    for index in range(2, stepNums + 1):
                        #获取第index行步骤对象
                        stepRow = excelObj.getRow(caseStepObj, index)
                        #获取关键字
                        keyWord = stepRow[testStep_keyWords - 1].value
                        #获取定位方式
                        locationType = stepRow[testStep_locationType - 1].value
                        #获取定位表达式
                        locatorExpression = stepRow[testStep_locatorExpression - 1].value
                        #获取操作值
                        operateValue = stepRow[testStep_operateValue - 1].value

                        if isinstance(operateValue,int):
                            operateValue = str(operateValue)

                        tmpStr = "'%s','%s'" %(locationType.lower(),locatorExpression.replace("'",'"')) if locationType and locatorExpression else ""

                        if tmpStr:
                            tmpStr += ",'" + operateValue + "'" if operateValue else ""
                        else:
                            tmpStr += "'" + operateValue + "'" if operateValue else ""

                        runStr = keyWord + "(" + tmpStr + ")"
                        print(runStr)

                        try:
                            #通过eval函数将字符串当成有效的python表达式执行
                            eval(runStr)
                        except Exception as e:
                            errorInfo = traceback.format_exc()
                            logging.debug("执行步骤 '%s' 时发生异常\n" %stepRow[testStep_testStepDescribe-1].value,errorInfo)
                            capturePic = capture_screen()
                            writeTestResult(caseStepObj, rowNo=index,colsNo="testStep", testResult="faild", errorInfo=str(errorInfo), picPath=capturePic)

                        else:
                            successfulSteps += 1
                            logging.info("执行步骤 '%s' 成功" %stepRow[testStep_testStepDescribe-1].value)
                            writeTestResult(caseStepObj, rowNo=index, colsNo="testStep", testResult="pass")

                    if successfulSteps == stepNums - 1:
                        successfulCase += 1
                        logging.info("用例 '%s' 执行通过" %caseName)
                        writeTestResult(caseSheet,rowNo=idx+2,colsNo="testCase",testResult="pass")
                    else:
                        logging.info("用例 '%s' 执行失败" %caseName)
                        writeTestResult(caseSheet,rowNo=idx+2,colsNo="testCase",testResult="faild")
                else:
                    #不需要执行的用例情况结果信息
                    writeTestResult(caseSheet,rowNo=idx+2,colsNo="testCase",testResult="")
                    logging.info("用例 ‘%s’ 被设置为忽略执行" %caseName)
        logging.info("共 %d 条用例， %d 条需要被执行，成功执行 %d 条" %(len(isExecuteColumn)-1,requiredCase,successfulCase))
    except Exception as e:
        logging.debug("程序本身发生异常\n %s" %traceback.format_exc())

if __name__ == '__main__':
    TestSendMailWithAttachment()