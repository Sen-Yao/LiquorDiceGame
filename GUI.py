
import sys
from PyQt5.QtWidgets import (QLabel, QDialog,QPushButton,QApplication,QLineEdit,QWidget)
from PyQt5.QtWidgets import (QHBoxLayout,QVBoxLayout,QCheckBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt



class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.user_input=None # 储存用户的输入
        self.is_open=False # 判断是否开
        self.is_jump_open=False # 判断是否跳开
        self.is_plus_one=False # 判断是否加一
        self.player_dice=[1,2,3,4,5] # 玩家骰子结果，测试用，实际从服务器读取
        self.current_player=1 # 玩家游戏序号，测试用，实际从服务器读取
        self.initWindow()

    # 初始化主窗口           
    def initWindow(self):               


        # 创建三个按钮供用户选择三种游戏策略
        openButton = QPushButton("开")
        continueButton = QPushButton("继续猜测")
        jumpButton = QPushButton("跳开")
        label = QLabel("欢迎使用LiquorDiceGame！\n您是" + str(self.current_player) +"号玩家" "\n您的骰子结果为" + ','.join(map(str, self.player_dice))+"\n请点击下方按钮做出您下一步的操作", self)


        # 对主界面进行盒布局
        hbox = QHBoxLayout()
        hbox.addWidget(openButton)
        hbox.addWidget(continueButton)
        hbox.addWidget(jumpButton)

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addLayout(hbox)
        self.setLayout(vbox) 

        
        # 根据按钮的点击情况选择不同的函数处理
        continueButton.clicked.connect(self.create_dialog)
        openButton.clicked.connect(self.open_action)
        jumpButton.clicked.connect(self.jump_open_action)

        # 设置窗口风格 大小图标
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('LiquorDiceGame')
        self.setWindowIcon(QIcon('./images/icon.png'))    
        self.show()
    
    # 该函数用于创建继续猜测的对话对象和读入用户输入
    def create_dialog(self):
        dialog = Dialog()
        result = dialog.exec_()  # 显示对话窗口并等待用户交互

        if result == QDialog.Accepted:
            # 用户点击了对话窗口的“确定”按钮
            self.user_input = dialog.get_user_input()
            print(f'用户输入的文本是: {self.user_input}')
            self.is_plus_one=dialog.verify_plus_one()
            print(f'用户是否加一:{self.is_plus_one}')
        # print(self.user_input)
    
    # 该函数用于处理开
    def open_action(self):
        self.is_open=True
        # print(self.is_open)
    
    # 该函数用于处理跳开
    def jump_open_action(self):
        self.is_jump_open=True
        # print(self.is_jump_open)


class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initDialog()
        self.user_input = None  # 初始化一个属性来保存用户输入
        self.is_plus_one = False # 初始化一个布尔型变量保存是否加一
    
    # 初始化对话栏 
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

        # 加一checkbox创立
        self.plus_one=QCheckBox('是否加一',self)
        layout.addWidget(self.plus_one)
        self.plus_one.toggle()
        self.plus_one.stateChanged.connect(self.verify_plus_one)

        # 添加“确定”按钮
        ok_button = QPushButton('确定', self)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)

    # 返回用户输入
    def get_user_input(self):
        return self.text_input.text()
    
    #返回用户勾选
    def verify_plus_one(self):
        if self.plus_one.checkState() == Qt.Checked:
            self.is_plus_one=True
        else:
            self.is_plus_one=False
        return self.is_plus_one


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())