#encoding = utf-8

from . import *

#测试用例或步骤执行完成后，写入执行结果信息
def writeTestResult(sheetObj,rowNo,colsNo,testResult,errorInfo=None,picPath=None):

    #测试通过结果为绿色，失败为红色
    colorDict = {"pass":"green","faild":"red","":None}

    #定义数组区分测试用例、测试步骤、测试数据中的执行时间和测试结果
    colsDict = {
        "testCase":[testCase_runTime,testCase_testResult],
        "testStep":[testStep_runTime,testStep_testResult],
        "dataSheet":[dataSource_runTime,dataSource_result]
    }

    try:
        # 在测试步骤sheet中写入测试结果
        excelObj.writeCell(sheetObj, content=testResult, rowNo=rowNo, colsNo=colsDict[colsNo][1],
                           style=colorDict[testResult])

        if testResult == "":
            #清空执行时间单元格
            excelObj.writeCell(sheetObj,content="",rowNo=rowNo,colsNo=colsDict[colsNo][0])
        else:
            # 在测试步骤sheet中写入测试时间
            excelObj.writeCellCurrentTime(sheetObj,rowNo=rowNo,colsNo=colsDict[colsNo][0])

        if errorInfo and picPath:
            # 在测试步骤sheet中写入异常信息
            excelObj.writeCell(sheetObj,content=errorInfo,rowNo=rowNo,colsNo=testStep_errorInfo)
            # 在测试步骤sheet中写入异常截图路径
            excelObj.writeCell(sheetObj,content=picPath,rowNo=rowNo,colsNo=testStep_errorPic)
        else:
            if colsNo == "caseStep":
                # 在测试步骤sheet中清空异常信息
                excelObj.writeCell(sheetObj,content="",rowNo=rowNo,colsNo=testStep_errorInfo)
                # 在测试步骤sheet中清空异常截图单元格
                excelObj.writeCell(sheetObj,content="",rowNo=rowNo,colsNo=testStep_errorPic)
    except Exception as e:
        print("写EXCEL时发生异常，",traceback.print_exc())