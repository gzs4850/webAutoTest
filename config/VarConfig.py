#encoding=utf-8
import os
ieDriverFilePath = "e:\geckodriver.exe"
chromeDriverFilePath = "e:\chromedriver.exe"
firefoxDriverFilePath = "e:\geckodriver.exe"

parentDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
screenPicturesDir = parentDirPath + "\\exceptionpictures\\"

# print(parentDirPath)
# print(screenPicturesDir)