import sys,re
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QLabel, QDialog, QPushButton, QApplication, QLineEdit, QWidget)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QCheckBox,QMessageBox)
from PyQt5.QtGui import QIcon,QIntValidator
from PyQt5.QtCore import Qt,QObject, pyqtSignal,QTimer
from web import libclient
from client.thread import New_Thread
import json





class Dialog(QDialog):
    def __init__(self,last_num,last_face,last_zhai):
        super().__init__()

        # 保存用户输入
        self.num = None
        self.face = None
        self.zhai = None

        # 上一个玩家猜测结果
        self.last_num = last_num
        self.last_face = last_face
        self.last_zhai = last_zhai

        self.is_use_one = None # 初始化一个布尔型变量保存是否喊一
        self.initDialog()
        
    
    # 初始化对话栏 
    def initDialog(self):
        self.setWindowTitle('继续猜测')
        self.setGeometry(200, 200, 300, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 对话引导提示符
        if self.last_num == -1:
            self.first_label = QLabel('你是第一个玩家,请输入你的猜测，以空格分隔(例如:7 4 1),最后一个数字0代表飞猜测，1代表斋猜测')
            self.layout.addWidget(self.first_label)
        else:
            self.then_label = QLabel('输入你的猜测，以空格分隔(例如:7 4 1),最后一个数字0代表飞猜测，1代表斋猜测:\n上一个玩家的猜测为：'+str(self.last_num)+' '+str(self.last_face)+' '+str(self.last_zhai),self)
            self.layout.addWidget(self.then_label)

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
        user_input = self.text_input.text()
        guess=user_input.split()
        # 将猜测值转化为整数（先前按照str格式保存）,同时检查输入的数字是否有效
        guess_quantity = int(guess[0])
        guess_value = int(guess[1])
        guess_rule = int(guess[2])
        return guess_quantity,guess_value,guess_rule
    
    # 验证用户文本输入
    def verify_input(self):
        user_input = self.text_input.text()

        # 使用正则表达式验证输入
        input_pattern = r'^[0-9]{1,2} [1-6] [0-1]$'  # 匹配输入要求
        if not re.match(input_pattern, user_input) :
            QMessageBox.warning(self, '错误', '输入不符合规范，请重新输入（例如：7 4 1）', QMessageBox.Ok)
            self.text_input.clear() # 清空文本框

        guess=user_input.split()
        # 将猜测值转化为整数（先前按照str格式保存）,同时检查输入的数字是否有效
        guess_quantity = int(guess[0])
        guess_value = int(guess[1])
        guess_rule = int(guess[2])

        # 用于判断输入是否正确
        ok_flag = True
        # 需要提供previous_guess
        if self.last_num != -1:  # 先前猜测不为空列表（本回合不是第一回合）
            last_guess_quantity = self.last_num
            last_guess_value = self.last_face
            last_rule = self.last_zhai
            # 检查猜的值是否符合基本规则
            # 如果为飞猜测
            if guess_rule == 0:
                if last_rule == 0:  # 上局为飞猜测，本局为飞猜测
                    if guess_quantity <= last_guess_quantity and guess_value <= last_guess_value or guess_value == 1:
                        QMessageBox.warning(self, '错误', '输入不符合斋飞规则，请重新输入', QMessageBox.Ok)
                        self.text_input.clear() # 清空文本框
                        ok_flag = False
                         
                if last_rule == 1:  # 上局为斋猜测，本局为飞猜测
                    if guess_quantity < last_guess_quantity * 2 and guess_value <= last_guess_value or guess_value == 1:
                        QMessageBox.warning(self, '错误', '输入不符合斋飞规则，请重新输入', QMessageBox.Ok)
                        self.text_input.clear() # 清空文本框
                        ok_flag = False
            else:
                if last_rule == 0:  # 上局为飞猜测，本局为斋猜测
                    if guess_quantity < int((last_guess_quantity + 1) / 2) and guess_value <= last_guess_value:
                        QMessageBox.warning(self, '错误', '输入不符合斋飞规则，请重新输入', QMessageBox.Ok)
                        self.text_input.clear() # 清空文本框
                        ok_flag = False
                if last_rule == 1:  # 上局为斋猜测，本局为斋猜测
                    if guess_quantity <= last_guess_quantity and guess_value <= last_guess_value:
                        QMessageBox.warning(self, '错误', '输入不符合斋飞规则，请重新输入', QMessageBox.Ok)
                        self.text_input.clear() # 清空文本框
                        ok_flag = False

        if ok_flag is True: 
            self.ok_button.setEnabled(True)

    #返回用户勾选
    def verify_use_one(self):
        if self.use_one.checkState() == Qt.Checked:
            self.is_use_one=True
        else:
            self.is_use_one=False
        return self.is_use_one

class Name_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.user_input = None  # 初始化一个属性来保存用户输入
        self.init_name_Dialog()
    
    def init_name_Dialog(self):
        self.setWindowTitle('输入用户名')
        self.setGeometry(200, 200, 300, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 对话引导提示符
        self.label = QLabel('输入你的用户名',self)
        self.layout.addWidget(self.label)

        # 文本编辑创立
        self.text_input = QLineEdit(self)
        self.layout.addWidget(self.text_input)

        # 添加“输入文本确定”按钮
        self.text_ok_button = QPushButton('确定输入', self)
        self.text_ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.text_ok_button)

    # 判断并返回用户输入
    def get_user_input(self):
        return self.text_input.text()