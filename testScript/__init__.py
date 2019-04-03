#encoding = utf-8

from action.PageAction import *
from util.ParseExcel import ParseExcel
from config.VarConfig import *
import time
import traceback

excelObj = ParseExcel()
excelObj.loadWorkBook(dataFilePath)