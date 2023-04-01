import json

from PyQt5.QtWidgets import QMdiArea
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QPushButton,QCheckBox,QFileDialog
from PySide2.QtUiTools import QUiLoader
from threading import Thread
from lib.share import SI, Mysingnals
import traceback

# 实例化
mysingnal_log = Mysingnals()


class Win_ai :

    def __init__(self):
        self.ui = QUiLoader().load('ai.ui')

    
    def onLog(self, msg):
        self.ui.text_log.append(msg)
        self.ui.text_log.ensureCursorVisible()


    def onReadExcel(self):
        # 创建pd对象
        import pandas as pd
        #选择文件
        fileName, fileType = QFileDialog.getOpenFileName(self.ui, "选取文件", "./data/browser_info.xlsx", "All Files (*);;Text Files (*.txt)")

        #读取文件
        data = pd.read_excel(fileName)
        #获取行数
        row = data.shape[0]
        #获取列数  
        column = data.shape[1]
        #设置表格行数
        self.ui.table_browser.setRowCount(row)
        #设置表格列数 
        self.ui.table_browser.setColumnCount(column+3)
        #设置表格头
        # self.ui.table_browser.setHorizontalHeaderLabels(self.CFG_ITEMS)
        #设置表格列宽
        self.ui.table_browser.setColumnWidth(0, 50)
        self.ui.table_browser.setColumnWidth(1, 200)
        self.ui.table_browser.setColumnWidth(2, 100)
        self.ui.table_browser.setColumnWidth(3, 100)
        self.ui.table_browser.setColumnWidth(4, 100)

        #设置表格内容 i 从1开始，因为第一行是表头
        for i in range(row):
            # 在第一列添加一个CheckBox
            qCheckBox = QCheckBox()
            qCheckBox.setChecked(True)
            self.ui.table_browser.setCellWidget(i, 0, qCheckBox)
            # 最后一列添加一个按钮
            button = QPushButton()
            button.setText("启动")
            self.ui.table_browser.setColumnWidth(5, 50)
            self.ui.table_browser.setCellWidget(i, 5, button)
            # 点击按钮调用消息框
            button.clicked.connect(self.onButtonClicked)

            btn_recreate = QPushButton()
            btn_recreate.setText("重建")

            self.ui.table_browser.setColumnWidth(6, 50)
            self.ui.table_browser.setCellWidget(i, 6, btn_recreate)
            # 点击按钮调用消息框
            btn_recreate.clicked.connect(self.onButtonClicked)
            # 从第二列开始共添加column列数据 即[1,column]
            for j in range(column):
                colIndex = j+1
                self.ui.table_browser.setItem(i,colIndex , QTableWidgetItem(str(data.iloc[i, j])))

        # 觸發信號 打印日志
        mysingnal_log.log.emit("读取Excel文件成功")
    def onButtonClicked(self):
        # 获取当前所选择的行
        row = self.ui.table_browser.currentRow()
        # 获取当前所选择的列
        column = self.ui.table_browser.currentColumn()
        # 消息框展示当前所选择的行和列
        QMessageBox.information(self.ui, "提示", "点击了第{}行第{}列".format(row, column))
        # 啓動子綫程來執行
        def threadFun():
            # 写到下面的日志框里面
            try:
                import subprocess
                mysingnal_log.log.emit(f"綫程已啓動......")
                node_exe_path = r'C:\Program Files\nodejs\node.exe'
                script_path = r'.\scripts\launch_browser_v2.js'
                datapath = r'.\data'

                main = [node_exe_path, script_path, f'--datapath={datapath}']
                p = subprocess.Popen(main, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                for line in p.stdout:
                    result = line.decode("utf-8")
                    mysingnal_log.log.emit(f"{result}")
            except:
                mysingnal_log.log.emit(f"綫程啓動失敗: \n" + traceback.format_exc())
        
        try:
            self.myThread = Thread(target=threadFun).start()
        except:
            mysingnal_log.log.emit(f"监测失败: \n" + traceback.format_exc())

