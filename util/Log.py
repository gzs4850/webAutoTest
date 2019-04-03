#encoding=utf-8
import logging.config
from config.VarConfig import parentDirPath

#读取日志配置文件
logging.config.fileConfig(parentDirPath+"\config\Logger.conf")
#选择一个日志格式
logger = logging.getLogger("example02")

def debug(message):
    logger.debug(message)

def info(message):
    logger.info(message)

def warning(message):
    logger.warning(message)
