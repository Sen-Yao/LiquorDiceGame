
import sys
from PyQt5.QtWidgets import (QLabel, QTextEdit,QDialog,QPushButton, QAction, QApplication,QLineEdit,QWidget)
from PyQt5.QtWidgets import (QHBoxLayout,QVBoxLayout,QInputDialog)
from PyQt5.QtGui import QIcon



class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.user_input=None # 储存用户的输入
        self.is_open=False # 判断是否开
        self.is_jump_open=False # 判断是否跳开
        self.is_plus_one=False # 判断是否加一
        self.initWindow()
        
        


    def initWindow(self):               


        # 创建两个按钮供用户选择
        openButton = QPushButton("开")
        continueButton = QPushButton("继续猜测")
        jumpButton = QPushButton("跳开")


        
        hbox = QHBoxLayout()
        hbox.addWidget(openButton)
        hbox.addWidget(continueButton)
        hbox.addWidget(jumpButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.setLayout(vbox) 
        
        # button connect to create dialog or open
        continueButton.clicked.connect(self.create_dialog)
        openButton.clicked.connect(self.open_action)
        jumpButton.clicked.connect(self.jump_open_action)

        # set the window's style
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('LiquorDiceGame')
        self.setWindowIcon(QIcon('./images/icon.png'))    
        self.show()
    
    def create_dialog(self):
        dialog = Dialog()
        result = dialog.exec_()  # 显示对话窗口并等待用户交互

        if result == QDialog.Accepted:
            # 用户点击了对话窗口的“确定”按钮
            self.user_input = dialog.get_user_input()
            print(f'用户输入的文本是: {self.user_input}')
        # print(self.user_input)
    
    def open_action(self):
        self.is_open=True
        # print(self.is_open)
    
    def jump_open_action(self):
        self.is_jump_open=True
        print(self.is_jump_open)


class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initDialog()
        self.user_input = None  # 初始化一个属性来保存用户输入

    def initDialog(self):
        self.setWindowTitle('继续猜测')
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        # 对话引导提示符
        self.label = QLabel('输入你的猜测，以空格分隔(例如:7 4 1),最后一个数字1代表飞猜测，2代表斋猜测:', self)
        layout.addWidget(self.label)


        # 文本编辑创立
        self.text_input = QLineEdit(self)
        layout.addWidget(self.text_input)

        # 添加“确定”按钮
        ok_button = QPushButton('确定', self)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        

        self.setLayout(layout)

    def get_user_input(self):
        return self.text_input.text()
    
        
    



        

        
        
        


    
        



            



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())