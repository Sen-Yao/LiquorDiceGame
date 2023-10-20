import sys,re
from PyQt5.QtWidgets import (QLabel, QDialog, QPushButton, QApplication, QLineEdit, QWidget)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QCheckBox, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.user_input=None # 储存用户的输入
        self.is_open = False # 判断是否开
        self.is_jump_open = False # 判断是否跳开
        self.is_guess = False # 判断是否继续猜测
        self.is_use_one=False # 判断是否喊一
        self.player_dice=[1,2,3,4,5] # 玩家骰子结果，测试用，实际从服务器读取
        self.current_player=1 # 玩家游戏序号，测试用，实际从服务器读取
        self.last_guess= [7,2,1] # 上一游戏玩家的猜测
        # 该变量储存实际上当前各玩家手上骰子的总和结果 依次代表有多少个1，2，3，4，5，6
        self.results=[6,6,6,6,6,6] 
        self.initWindow()

    # 初始化主窗口           
    def initWindow(self):
        # 创建三个按钮供用户选择三种游戏策略
        openButton = QPushButton("开")
        continueButton = QPushButton("继续猜测")
        jumpButton = QPushButton("跳开")
        label = QLabel(
            "欢迎使用LiquorDiceGame！\n您是" + str(self.current_player) + "号玩家" "\n您的骰子结果为" + ','.join(
                map(str, self.player_dice)) +"\n上一玩家猜测结果为" + ','.join(map(str, self.last_guess))+ "\n请点击下方按钮做出您下一步的操作", self)

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
        self.is_guess = True
        dialog = Dialog()
        result = dialog.exec_()  # 显示对话窗口并等待用户交互

        if result == QDialog.Accepted:
            # 用户点击了对话窗口的“确定”按钮
            self.user_input = dialog.get_user_input()
            print(f'用户输入的文本是: {self.user_input}')
            self.is_use_one=dialog.verify_use_one()
            print(f'用户是否喊一:{self.is_use_one}')
        # print(self.user_input)

    # 该函数用于处理开
    def open_action(self):
        self.is_open = True
        self.show_results()
        
    # 该函数用于处理跳开
    def jump_open_action(self):
        self.is_jump_open = True
        self.show_results()

    # 该函数用于展示结果
    def show_results(self):
        # 创建展示窗口
        show_window = QDialog()

        # 展示结果标签
        results_label = QLabel(self)
        results_text = '最后各玩家的总结果为 '
        for index, nums in enumerate(self.results):
            results_text += f'{nums}个{index+1} '
        results_label.setText(results_text)
        
        # 对子窗口进行盒布局
        hbox = QHBoxLayout()
        hbox.addWidget(results_label)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        show_window.setLayout(vbox)

        # 设计窗口并显示
        show_window.setWindowTitle('结果展示')
        show_window.setGeometry(200, 200, 300, 200)
        show_window.show()
        show_window.exec_()


class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initDialog()
        self.user_input = None  # 初始化一个属性来保存用户输入
        self.is_use_one = False # 初始化一个布尔型变量保存是否喊一
    
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

        # 喊一checkbox创立
        self.use_one=QCheckBox('是否喊一',self)
        layout.addWidget(self.use_one)
        self.use_one.toggle()
        self.use_one.stateChanged.connect(self.verify_use_one)

        # 添加“确定”按钮
        ok_button = QPushButton('确定', self)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    # 判断并返回用户输入
    def get_user_input(self):
        user_input = self.text_input.text()
        # 使用正则表达式验证输入
        input_pattern = r'^\d+\s\d+\s\d+$'  # 匹配三个带空格的数字
        if not re.match(input_pattern, user_input):
            QMessageBox.warning(self, '错误', '输入不符合规范，请重新输入（例如：7 4 2）', QMessageBox.Ok)
            self.text_input.clear()  # 清空文本框

        return self.text_input.text()
    
    #返回用户勾选
    def verify_use_one(self):
        if self.use_one.checkState() == Qt.Checked:
            self.is_use_one=True
        else:
            self.is_use_one=False
        return self.is_use_one

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
