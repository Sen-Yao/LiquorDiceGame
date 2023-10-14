
"""
GUI整体设计思路
1.创建一个GUI,用户使用时需要提供的交互式操作为：
    1. 根据主函数中游戏人数的循环计算出是否轮到当前玩家做猜测，并提供给定的交互式窗口，该窗口要做的是显示提示语和将用户的输入(包括基本输入和斋飞)读入到主程序，并提供一个是否喊一的二选一按钮
    2. 是否跳开（如果跳开，立即调用函数计算当前规则下的结果），并将主程序的当前玩家更新

2. mytask:创建窗口并布局    
"""


import sys
from PyQt5.QtWidgets import (QMainWindow,QLabel, QTextEdit,QInputDialog,QPushButton, QAction, QApplication,QLineEdit,QWidget)
from PyQt5.QtGui import QIcon



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initWindow()
        
        


    def initWindow(self):               

        # create a tool to exit
        exitAct = QAction(QIcon('./images/exit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()

        # creare menuBar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)

        # create the dialog button to guide input

        inputbtn=QPushButton('开始游戏',self)
        inputbtn.setToolTip('点击即可开始游戏')
        inputbtn.resize(inputbtn.sizeHint())
        inputbtn.move(100, 100) 
        
        # button connect to create dialog
        inputbtn.clicked.connect(self.create_dialog)
        

        # set the window's style
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('LiquorDiceGame')
        self.setWindowIcon(QIcon('./images/icon.png'))    
        self.show()
    
    def create_dialog(self):
        self.dialog=Dialog()
        
        
        
        
        





class Dialog(QWidget):

    def __init__(self):
        super().__init__()
        self.user_input = None  # 初始化一个属性来保存用户输入
        self.stored_text = None  # 初始化一个属性来保存打印的文本
        self.initDialog()
        
        


    def initDialog(self):

        self.btn = QPushButton('输入猜测', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)


        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('输入猜测')
        self.show()


    def showDialog(self):

        text, ok = QInputDialog.getText(self, '输入猜测', 
            '输入你的猜测，以空格分隔(例如:7 4 1),最后一个数字1代表飞猜测，2代表斋猜测:')
        if ok:
            self.le.setText(str(text))
            print(f'用户输入的文本是: {text}')
            

    
    
    


            



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())