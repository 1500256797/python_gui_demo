from PyQt5.QtWidgets import QMdiArea
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMessageBox, QMdiSubWindow, QTreeWidgetItem
from PySide2.QtUiTools import QUiLoader

from lib.share import SI
from cfg import Win_CfgConnection
from browser_automate import Win_BrowserAutomate
from ai import Win_ai
class Win_Main :

    def __init__(self):
        self.ui = QUiLoader().load('main.ui')


        self.ui.action_wallet.triggered.connect(self.onWalletTree)
        self.ui.action_connection.triggered.connect(self.onCfgConnection)

        #树节点双击操作
        self.ui.opTree.itemDoubleClicked.connect(self.opTreeAction)

        # 默认打开action_wallet
        self.onWalletTree()
        # 默认双击打开第一个目录的第一个节点
        self.opTreeAction(self.ui.opTree.topLevelItem(0).child(0),0)

    def onCfgConnection(self):
        '''
        在此函数中主要实现，在子窗口区，如果把窗口弹出来。
        :return:
        '''
        self._openSubMin(Win_CfgConnection)

    def _openSubMin(self,FuncClass):
        '''
        多次点击按钮 只打开同一个窗口的实现方式
        :param FuncClass:
        :return:
        '''
        def createSubWin():
            subWindowFunc = FuncClass()
            subWin = QMdiSubWindow() #子窗口框子
            subWin.setWidget(subWindowFunc.ui)
            subWin.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.ui.mdiArea.addSubWindow(subWin)
            #存入表中 ，注意winFunc对象也要存，不然对象没用引用，会销毁
            SI.subWinTable[str(FuncClass)] = {'subWin':subWin,'subWinFunc':subWindowFunc}
            subWin.show()
            # 子窗口提到最上层，并且最大化
            subWin.setWindowState(Qt.WindowActive | Qt.WindowMaximized)
        #如果该功能类型实例不存在 str化
        if str(FuncClass) not in SI.subWinTable:
            #创建实例
            createSubWin()
            return
        #如果已经存在 则直接show
        subWin = SI.subWinTable[str(FuncClass)]['subWin']
        try:
            subWin.show()
            # 子窗口提到最上层，并且最大化
            subWin.setWindowState(Qt.WindowActive | Qt.WindowMaximized)
        except:
            #show 异常，异常原因肯定是用户手动关闭了该窗口，subWin对象不存在了
            createSubWin()

    def opTreeAction(self,item,column):
        '''
        # 参数 item 是被点击节点对应的 QTreeWidgetItem 对象
        # 参数 column 是被点击的column号
        http://v3.byhy.net/tut/py/gui/qt_05_4/#%E4%BF%A1%E5%8F%B7%E5%A4%84%E7%90%86
        :param item:
        :param column:
        :return:
        '''
        # 获取被点击的节点文本
        clickedText = item.text(column)
        if clickedText not in  self.opTreeActionTable:
            return
        actionWinFunc = self.opTreeActionTable[clickedText]
        self._openSubMin(actionWinFunc)


    def onWalletTree(self):
        '''
        树的这块操作，基本上没有qt designer什么事
        :return:
        '''
        self.ui.opTree.setVisible(True)
        # 先清空树节点
        self.ui.opTree.clear()

        root = self.ui.opTree.invisibleRootItem() #找到树的根节点 这个在界面上不可见
        # 创建一个 目录节点
        folderItem = QTreeWidgetItem()
        # 设置该节点  第1个column 文本
        folderItem.setText(0, '浏览器')
        root.addChild(folderItem)  # 添加到树的不可见根节点下，就成为第一层节点
        folderItem.setExpanded(True)  # 设置该节点为展开状态

        leafItem = QTreeWidgetItem()  # 叶子 节点
        leafItem.setText(0, '管理浏览器')  # 设置该节点  第1个column 文本
        folderItem.addChild(leafItem)  # 添加到目录节点中


        # 创建一个 目录节点
        folderItem = QTreeWidgetItem()
        folderItem.setText(0, 'AI模型')
        folderItem.setExpanded(True)  # 设置该节点为展开状态
        root.addChild(folderItem)  # 添加到树的不可见根节点下，就成为第一层节点

        leafItem = QTreeWidgetItem()  # 叶子 节点
        leafItem.setText(0, '打开ai模型')  # 设置该节点  第1个column 文本
        folderItem.addChild(leafItem)  # 添加到目录节点中


        # 维护一张操作树界面表，维护item和功能区的对应关系
        self.opTreeActionTable = {
            '管理浏览器': Win_BrowserAutomate,
            '打开ai模型': Win_ai
        }

#流程，ui，菜单栏、mdi子窗口
SI.loadCfgFile()# 程序启动就加载配置文件
app = QApplication([])
SI.loginWin = Win_Main()
SI.loginWin.ui.show()
app.exec_()