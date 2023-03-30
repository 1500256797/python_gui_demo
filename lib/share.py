import json
import os.path

from PySide2.QtCore import QObject, Signal


class SI:
    mainWin = None
    login = None
    session = None #全局共享session
    #系统配置,包括后端地址、IP等
    cfg={}

    #保存mdi子窗口对象
    subWinTable = {}
    #静态方法
    @staticmethod
    def loadCfgFile():
        if os.path.exists("cfg.json"):
            with open('cfg.json',encoding="utf8") as f:
                SI.cfg = json.load(f)

# 自定义信号源对象类型，一定要继承自QObject
class Mysingnals(QObject):
    # 定义一种信号名叫log，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    log = Signal(str)