import sys,re
from PyQt5.QtWidgets import (QLabel, QDialog, QPushButton, QApplication, QLineEdit, QWidget)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QCheckBox,QMessageBox)
from PyQt5.QtGui import QIcon,QIntValidator
from PyQt5.QtCore import Qt


class GUI(QWidget):

    def __init__(self,player_dice,current_player,last_guess,counts,results,is_action,previous_guess):
        super().__init__()
        self.user_input=None # 储存用户的输入
        self.is_open = False # 判断是否开
        self.is_jump_open = False # 判断是否跳开
        self.is_guess = False # 判断是否继续猜测
        self.is_use_one=False # 判断是否喊一

        self.is_action=is_action # 根据传入变量，判断现在是否轮到当前玩家        
        self.player_dice=player_dice # 玩家骰子结果,从服务器读取
        self.current_player=current_player # 玩家游戏序号,从服务器读取
        self.last_guess= last_guess# 上一游戏玩家的猜测
        self.previous_guess=previous_guess # 记录过去所有玩家的猜测
        # 该变量储存实际上当前各玩家手上骰子的总和结果 依次代表有多少个1，2，3，4，5，6
        self.counts=counts
        self.results=results # 该变量储存开出来的胜负结果

        self.initWindow()

    # 初始化主窗口           
    def initWindow(self):
        # 创建三个按钮供用户选择三种游戏策略
        openButton = QPushButton("开")
        continueButton = QPushButton("继续猜测")
        jumpButton = QPushButton("跳开")
        # 未到当前玩家时开和猜测不能用
        openButton.setEnabled(False)
        continueButton.setEnabled(False)


        welcome_label = QLabel(
            "欢迎使用LiquorDiceGame！\n您是" + str(self.current_player) + "号玩家" "\n您的骰子结果为" + ','.join(
                map(str, self.player_dice)) +"\n上一玩家猜测结果为" + ','.join(map(str, self.last_guess)), self)
        no_action_label = QLabel("\n当前未到您的轮次，但您可以选择跳开")
        action_label=QLabel("\n当前轮到您的轮次，请从下面三个按钮中选择您要进行的操作")
        
        # 对主界面进行盒布局
        hbox = QHBoxLayout()
        hbox.addWidget(openButton)
        hbox.addWidget(continueButton)
        hbox.addWidget(jumpButton)

        vbox = QVBoxLayout()
        vbox.addWidget(welcome_label)
        # 根据顺序判断添加操作
        if self.is_action is True:
            vbox.addWidget(action_label)
            openButton.setEnabled(True)
            continueButton.setEnabled(True)
        else:
            vbox.addWidget(no_action_label)
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
        dialog = Dialog(self.previous_guess,self.current_player,self.last_guess)
        result = dialog.exec_()  # 显示对话窗口并等待用户交互

        if result == QDialog.Accepted and dialog.get_user_input is not None:
            # 用户点击了对话窗口的“确定”按钮
            self.user_input = dialog.get_user_input()
            print(f'用户输入的文本是: {self.user_input}')
            self.is_use_one=dialog.verify_use_one()
            print(f'用户是否喊一:{self.is_use_one}')
        print(self.user_input)

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
        all_results_label = QLabel(self)
        all_results_text = '最后各玩家的总结果为 '
        for index, nums in enumerate(self.counts):
            all_results_text += f'{nums}个{index+1} '
        all_results_label.setText(all_results_text)

        win_label=QLabel(self,text="你的开猜测为真！你赢得游戏！")
        loss_label=QLabel(self,text="你的开猜测为假！你输掉游戏！")
        # 对子窗口进行盒布局
        hbox = QHBoxLayout()
        hbox.addWidget(all_results_label)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        if self.results is True:
            vbox.addWidget(win_label)
        else:
            vbox.addWidget(loss_label)
        show_window.setLayout(vbox)

        # 设计窗口并显示
        show_window.setWindowTitle('结果展示')
        show_window.setGeometry(200, 200, 300, 200)
        show_window.show()
        show_window.exec_()


class Dialog(QDialog):
    def __init__(self,previous_guess,current_player,last_guess):
        super().__init__()

        self.user_input = None  # 初始化一个属性来保存用户输入
        self.is_use_one = False # 初始化一个布尔型变量保存是否喊一
        self.previous_guess=previous_guess # 记录过去所有玩家的猜测
        self.current_player=current_player # 玩家游戏序号,从服务器读取
        self.last_guess= last_guess# 上一游戏玩家的猜测
        self.initDialog()
        
    
    # 初始化对话栏 
    def initDialog(self):
        self.setWindowTitle('继续猜测')
        self.setGeometry(200, 200, 300, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 对话引导提示符
        self.label = QLabel('输入你的猜测，以空格分隔(例如:7 4 1),最后一个数字0代表飞猜测，1代表斋猜测:\n上一个玩家的猜测为'+str(self.last_guess), self)
        self.layout.addWidget(self.label)

        # 文本编辑创立
        self.text_input = QLineEdit(self)
        self.layout.addWidget(self.text_input)

        # 喊一checkbox创立
        self.use_one=QCheckBox('是否喊一',self)
        self.layout.addWidget(self.use_one)
        self.use_one.toggle()
        self.use_one.stateChanged.connect(self.verify_use_one)

        # 添加“输入文本确定”按钮
        self.text_ok_button = QPushButton('确定输入', self)
        self.text_ok_button.clicked.connect(self.verify_input)
        self.layout.addWidget(self.text_ok_button)

        # 添加“最终确定”按钮（只有文本按钮对才能最终确定）
        self.ok_button = QPushButton('最终确定', self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        self.ok_button.setEnabled(False)

    # 判断并返回用户输入
    def get_user_input(self):
        return self.text_input.text()
    
    # 验证用户文本输入
    def verify_input(self):
        user_input = self.text_input.text()

        # 使用正则表达式验证输入
        input_pattern = r'^[0-3][0-9] [1-6] [0-1]$'  # 匹配输入要求
        if not re.match(input_pattern, user_input) :
            QMessageBox.warning(self, '错误', '输入不符合规范，请重新输入（例如：7 4 1）', QMessageBox.Ok)
            self.text_input.clear() # 清空文本框

        guess=user_input.split()
        # 将猜测值转化为整数（先前按照str格式保存）,同时检查输入的数字是否有效
        guess_quantity = int(guess[0])
        guess_value = int(guess[1])
        guess_rule = int(guess[2])

        if self.previous_guess != []:  # 先前猜测不为空列表（本回合不是第一回合）
            last_guess = self.previous_guess[-1]  # 上一个玩家的猜测
            last_guess_quantity = int(last_guess[0])
            last_guess_value = int(last_guess[1])
            last_rule = int(last_guess[2])
            # 检查猜的值是否符合基本规则
            # 如果为飞猜测
            if guess_rule == 0:
                if last_rule == 0:  # 上局为飞猜测，本局为飞猜测
                    if guess_quantity <= last_guess_quantity and guess_value <= last_guess_value or guess_value == 1:
                        QMessageBox.warning(self, '错误', '输入不符合斋飞规则，请重新输入', QMessageBox.Ok)
                        self.text_input.clear() # 清空文本框
                         
                if last_rule == 1:  # 上局为斋猜测，本局为飞猜测
                    if guess_quantity < last_guess_quantity * 2 and guess_value <= last_guess_value or guess_value == 1:
                        QMessageBox.warning(self, '错误', '输入不符合斋飞规则，请重新输入', QMessageBox.Ok)
                        self.text_input.clear() # 清空文本框
            else:
                if last_rule == 0:  # 上局为飞猜测，本局为斋猜测
                    if guess_quantity < int((last_guess_quantity + 1) / 2) and guess_value <= last_guess_value:
                        QMessageBox.warning(self, '错误', '输入不符合斋飞规则，请重新输入', QMessageBox.Ok)
                        self.text_input.clear() # 清空文本框
                if last_rule == 1:  # 上局为斋猜测，本局为斋猜测
                    if guess_quantity <= last_guess_quantity and guess_value <= last_guess_value:
                        QMessageBox.warning(self, '错误', '输入不符合斋飞规则，请重新输入', QMessageBox.Ok)
                        self.text_input.clear() # 清空文本框 

        guess[2] = bool(guess_rule)  # 把1或0转化为bool值，false代表飞猜，true代表斋猜
        guess.append(self.current_player)  # 把玩家信息加入列表中，以便标识谁做出的猜测
        self.previous_guess.append(guess)  # 做出正确猜测后将该猜测存入列表
        self.ok_button.setEnabled(True)

    #返回用户勾选
    def verify_use_one(self):
        if self.use_one.checkState() == Qt.Checked:
            self.is_use_one=True
        else:
            self.is_use_one=False
        return self.is_use_one
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # use to test
    ex = GUI(player_dice=[1,1,1,1,1,1],current_player=1,last_guess=[7,4,1],counts=[6,6,6,6,6,6],results=False,is_action=True,previous_guess=[['7','4',True,'玩家1']])
    sys.exit(app.exec_())
