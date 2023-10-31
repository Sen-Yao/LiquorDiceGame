import sys,re
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QLabel, QDialog, QPushButton, QApplication, QLineEdit, QWidget)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QCheckBox,QMessageBox)
from PyQt5.QtGui import QIcon,QIntValidator
from PyQt5.QtCore import Qt,QObject, pyqtSignal,QTimer
from web import libclient
import json


class GUI(QWidget):
    data_received = pyqtSignal(str)  # 定义一个自定义信号，用于接收外部实时输入的字符串信息
    def __init__(self):
        super().__init__()
        self.type = None
        self.data_received.connect(self.update_gui)  # 将自定义信号连接到update_gui槽函数
        # start_mesg type
        self.current_round = None
        self.dice = None
        self.player_id = None
        self.player_name = None
        # 当传入的字典type为ask
        
        self.is_your_round = None
        self.num = None
        self.face = None
        self.zhai = None    # 分别储存用户具体猜测
        # 储存上一个用户的猜测
        self.last_num = None
        self.last_face = None
        self.last_zhai = None

        self.user_input = None  # 储存用户的猜测输入
        self.is_open = None  # 判断是否开
        self.is_jump_open = None  # 判断是否跳开
        self.is_guess = None  # 判断是否进行猜测
        self.is_use_one = None  # 判断是否喊一 
              

        # 当传入的字典type为end
        
        self.dices = None # 最终结果
        self.names = None # 最终玩家姓名
        self.info = None
        
        self.initWindow()

    # 初始化主窗口           
    def initWindow(self):
        
        self.name_welcome_label = QLabel("尊敬的玩家，您好！\n")
        self.welcome_label = QLabel("欢迎使用LiquorDiceGame！,当前游戏暂未开始\n")
        # start_mesg 
        if self.type == 'start_mesg':
            self.welcome_label = QLabel(
            "欢迎使用LiquorDiceGame！\n,当前游戏轮次为第"+str(self.current_round)+",您是" + str(self.player_id) + "号玩家" "\n您的骰子结果为" + ','.join(
                map(str, self.dice))+"\n当前未到您的轮次，请您耐心等待!" , self)
            self.welcome_label.setVisible(False)
        # broadcast_mesg
        if self.type == 's2c_decide':
            self.broadcast_label = QLabel("现在"+str(self.player_id)+"号玩家"+str(self.player_name)+"的猜测结果是"+str(self.num)+str(self.face)+str(self.zhai)+"请您参考并等待进行下一步操作")
            self.broadcast_label.setVisible(False)
        # end_mesg
        if self.type == 'end':
            self.end_label = QLabel("游戏结束，各玩家的结果为"+str(self.dices)+"\n参与本轮游戏的玩家为"+str(self.names))
            self.end_info = QLabel(self.info)
            self.end_label.setVisible(False)
            self.end_info.setVisible(False)
        # 创建按钮供用户选择两种游戏策略（ask）
        self.openButton = QPushButton("开")
        self.continueButton = QPushButton("继续猜测")
        self.action_label=QLabel("\n当前轮到您的轮次，请从下面两个按钮中选择您要进行的操作")
       
        # 对主界面进行盒布局
        hbox = QHBoxLayout()
        hbox.addWidget(self.openButton)
        hbox.addWidget(self.continueButton)
        # 根据按钮的点击情况选择不同的函数处理
        self.continueButton.clicked.connect(self.create_dialog)
        self.openButton.clicked.connect(self.open_action)
        vbox = QVBoxLayout()
        vbox.addWidget(self.name_welcome_label)
        vbox.addWidget(self.welcome_label)
        vbox.addWidget(self.action_label)
        if self.type == 'start_mesg':
            vbox.addWidget(self.welcome_label)
        if self.type == 's2c_decide':
            vbox.addWidget(self.broadcast_label)
        if self.type == 'end':
            vbox.addWidget(self.end_label)
            vbox.addWidget(self.end_info)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        # 设置窗口风格 大小图标
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('LiquorDiceGame')
        self.setWindowIcon(QIcon('./images/icon.png'))

    # 该函数用于创建继续猜测的对话对象和读入用户输入
    def create_dialog(self):
        dialog = Dialog(self.last_num,self.last_face,self.last_zhai)
        result = dialog.exec_()  # 显示对话窗口并等待用户交互

        if result == QDialog.Accepted and dialog.get_user_input is not None:
            # 用户点击了对话窗口的“确定”按钮
            self.num,self.face,self.zhai = dialog.get_user_input()
            self.is_use_one=dialog.verify_use_one()

    def update_gui(self,read_server_str):
        # # convert json's type to dict
        read_server_fn = json.loads(read_server_str)
        if read_server_fn['type'] == 'start_mesg':
            self.type = 'start_mesg'
            self.current_round = read_server_fn['current_round']
            self.dice = read_server_fn['dice']
            self.player_id = read_server_fn['player_id']
            self.player_name = read_server_fn['player_name']

            self.name_welcome_label.setText(str(self.player_name)+'您好!\n')
            self.welcome_label.setText(
            "欢迎使用LiquorDiceGame！\n,当前游戏轮次为第"+str(self.current_round)+",您是" + str(self.player_id) + "号玩家" "\n您的骰子结果为" + ','.join(
                map(str, self.dice))+"\n当前未到您的轮次，请您耐心等待!" )
            
        elif read_server_fn['type'] == 'Ask':
            self.type = 'Ask'
            self.openButton.setVisible(True)
            self.continueButton.setVisible(True)
            self.action_label.setVisible(True)
            # set others widget false
            # self.welcome_label.setVisible(False)
            # 储存上一个用户的猜测
            self.last_num = read_server_fn['last_guess_num']
            self.last_face = read_server_fn['last_guess_face']
            self.last_zhai = read_server_fn['last_guess_zhai']
            # 玩家继续猜测的输入，用于返回到服务器端
            if read_server_fn['type'] == 'Ask':
                decide = {
                    'type': 'decide',
                    'num': self.num,  # 若为0则代表玩家选择开
                    'face': self.face,
                    'zhai': self.zhai
                }
                decide_mesg_json = json.dumps(decide)
                # write_server(decide_mesg_json)
        elif read_server_fn['type'] == 's2c_decide':
            self.type = 's2c_decide'
            self.broadcast_label.setVisible(True)
            self.player_id = read_server_fn['player_id'] # 广播用户id
            self.player_name = read_server_fn['player_name'] # 广播用户name
            self.num = read_server_fn['num'] # 广播用户猜测
            self.face = read_server_fn['face']
            self.zhai = read_server_fn['zhai']
        elif read_server_fn['type'] == 'end':
            self.type = 'end'
            self.dices = read_server_fn['dice'] # 最终结果
            self.names = read_server_fn['name'] # 最终玩家姓名
            self.info = read_server_fn['info'] 

                
            
            

    # 该函数用于处理开
    def open_action(self):
        self.is_open = True
        self.num = 0    

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
        input_pattern = r'^[0-9] [1-6] [0-1]$'  # 匹配输入要求
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


# 该函数用于创建用户名
def create_name():
    name_dialog = Name_dialog()
    result = name_dialog.exec_()  # 显示对话窗口并等待用户交互

    if result == QDialog.Accepted and name_dialog.get_user_input is not None:
        # 用户点击了对话窗口的“确定”按钮
        player_name = name_dialog.get_user_input()
        # print(f'用户输入的文本是: {self.player_name}')
        return player_name
    

        


def main_client():
    app = QApplication(sys.argv) 
    # create name to client
    read_server,write_server = libclient.get_remote_fn(server_ip='127.0.0.1', server_port=12347)
    client=GUI()
    client.show()
    player_name = create_name()
    write_server(player_name)
    # read from server
    success_connect_str = read_server()
    print(success_connect_str)
    while True:
        read_server_str = read_server()
        print(read_server_str)
        # 将json字符串传入GUI
        client.data_received.emit(read_server_str)

    
    sys.exit(app.exec_())



if __name__ == '__main__':
    main_client()
    
