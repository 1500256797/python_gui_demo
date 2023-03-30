import json

from PyQt5.QtWidgets import QMdiArea
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PySide2.QtUiTools import QUiLoader

# import requests

from lib.share import SI


class Win_CfgConnection :
    # 此配置表格中的内容项是固定的 所以写死在代码里
    CFG_ITEMS = [
        'web服务地址',"web服务端口","数据库服务地址","数据库服务端口",'数据库连接账户',"数据库连接密码"
    ]

    def __init__(self):
        self.ui = QUiLoader().load('cfg.ui')
        self.loadCfgToTable()
        # 指定单元格改动信号处理函数
        self.ui.table_cfg.cellChanged.connect(self.cfgItemChanged)
        self.ui.btn_clearLog.clicked.connect(self.onClearLog)

    def onClearLog(self):
        self.ui.text_log.clear()

    def loadCfgToTable(self):
        '''
        定义函数把配置文件中的配置项加载到界面表格里
        :return:
        '''
        table = self.ui.table_cfg
        for idx,cfgName in enumerate(self.CFG_ITEMS):
            # 插入一行
            table.insertRow(idx)
            # 参数名
            item = QTableWidgetItem(cfgName)
            item.setFlags(Qt.ItemIsEnabled) # 参数名字段不允许修改
            table.setItem(idx, 0, item) #idx行 0列
            #参数值
            table.setItem(idx,1,QTableWidgetItem(SI.cfg.get(cfgName,'')))#表格为空 要这么写

    def cfgItemChanged(self, row, column):
        # 获取更改内容
        cfgName = self.ui.table_cfg.item(row, 0).text()  # 首列为配置名称
        cfgValue = self.ui.table_cfg.item(row, column).text()
        SI.cfg[cfgName] = cfgValue # 存放到内存中
        #把改动的结果存到文件里，流行的方式是json
        self._saveCfgFile()
        # 写到下面的日志框里面
        self.ui.text_log.append("{} 已更新为 【{}】 ".format(cfgName,cfgValue))
        self.ui.text_log.ensureCursorVisible()
    def _saveCfgFile(self):
        '''
        外来信号直接调用不加下划线，内部调用的加下划线
        :return:
        '''
        table = self.ui.table_cfg
        cfg = {}
        # for lineNo in range(table.rowCount()):
        #     # 获取更改内容
        #     cfgName = self.ui.table_cfg.item(lineNo, 0).text()  # 首列为配置名称
        #     cfgValue = self.ui.table_cfg.item(lineNo, 1).text()
        #     cfg[cfgName] = cfgValue
        with open('cfg.json','w',encoding='utf8') as f:
            json.dump(SI.cfg,f,ensure_ascii=False,indent=2)