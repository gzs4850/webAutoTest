#encoding = utf-8

import win32clipboard as w
import win32com

class Clipboard(object):
    @staticmethod
    def getText():
        w.OpenClipboard()
        d = w.GetClipboardData(win32com.CF_TEXT)
        w.CloseClipboard()
        return d

    @staticmethod
    def setText(aString):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32com.CF_UNICODETEXT,aString)
        w.CloseClipboard()