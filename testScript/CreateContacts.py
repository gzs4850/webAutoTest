#encoding=utf-8
from . import *
from .WriteTestResult import writeTestResult
from util.Log import *

def dataDriverFun(dataSourceSheetObj,stepSheetObj):
    try:
        #获取是否执行对象
        dataIsExecuteColumn = excelObj.getColumn(dataSourceSheetObj,dataSource_isExecute)
        #获取email对象
        emailColumn = excelObj.getColumn(dataSourceSheetObj,dataSource_email)
        #获取测试步骤表中存在数据区域的行数
        stepRowNums = excelObj.getRowsNumber(stepSheetObj)
        #记录成功执行的数据条数
        successDatas = 0
        #记录需要执行的数据条数
        requiredDatas = 0

        for idx,data in enumerate(dataIsExecuteColumn[1:]):
            #遍历数据表
            if data.value == "y":
                logging.info("开始添加联系人 %s" %emailColumn[idx+1].value)
                requiredDatas += 1
                #记录执行成功步骤条数
                successStep = 0

                for index in range(2,stepRowNums + 1):
                    #获取数据驱动测试步骤表中第index行对象
                    rowObj = excelObj.getRow(stepSheetObj,index)
                    #获取关键字
                    keyWord = rowObj[testStep_keyWords - 1].value
                    #获取定位方式
                    locationType = rowObj[testStep_locationType - 1].value
                    #获取定位表达式
                    locatorExpression = rowObj[testStep_locatorExpression - 1].value
                    #获取操作值
                    operateValue = rowObj[testStep_operateValue - 1].value
                    if isinstance(operateValue, int):
                        operateValue = str(operateValue)

                    if operateValue and operateValue.isalpha():
                        coordinate = operateValue + str(idx+2)
                        print("coordinate:%s" %coordinate)
                        operateValue = excelObj.getCellOfValue(dataSourceSheetObj,coordinate=coordinate)

                    tmpStr = "'%s','%s'" %(locationType.lower(),locatorExpression.replace("'",'"')) if locationType and locatorExpression else ""

                    if tmpStr:
                        tmpStr += ",'" + operateValue +"'" if operateValue else ""
                    else:
                        tmpStr += "'" + operateValue + "'" if operateValue else ""

                    runStr = keyWord + "(" + tmpStr + ")"
                    print(runStr)

                    try:
                        if operateValue != "否":
                            eval(runStr)
                    except Exception as e:
                        logging.info("执行步骤 '%s' 发生异常" %rowObj[testStep_testStepDescribe - 1].value,traceback.print_exc())
                    else:
                        successStep += 1
                        logging.info("执行步骤 '%s' 成功" %rowObj[testStep_testStepDescribe - 1].value)

                if stepRowNums == successStep + 1:
                    successDatas += 1
                    #写入成功信息
                    writeTestResult(sheetObj=dataSourceSheetObj,rowNo=idx+2,colsNo="dataSheet",testResult="pass")
                else:
                    #写入失败信息
                    writeTestResult(sheetObj=dataSourceSheetObj,rowNo=idx+2,colsNo="dataSheet",testResult="faild")
            else:
                #不需要执行的清空结果信息
                writeTestResult(sheetObj=dataSourceSheetObj,rowNo=idx+2,colsNo="dataSheet",testResult="")

        if requiredDatas == successDatas:
            #需要执行的数据行与成功个数一致时，返回1，否则返回0
            return 1
        return 0
    except Exception as e:
        raise e



