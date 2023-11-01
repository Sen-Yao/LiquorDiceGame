import sys,re
import time
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QLabel, QDialog, QPushButton, QApplication, QLineEdit, QWidget)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QCheckBox,QMessageBox)
from PyQt5.QtGui import QIcon,QIntValidator
from PyQt5.QtCore import Qt,QObject, pyqtSignal,QTimer
from web import libclient
from client.thread import New_Thread
from client.used_class import Dialog
from client.used_class import Name_dialog
import json


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.type = None
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
        self.finish_decide = None # 判断是否结束猜测 
              

        # 当传入的字典type为end
        
        self.dices = None # 最终结果
        self.names = None # 最终玩家姓名
        self.info = None
        
        self.initWindow()

    # 初始化主窗口           
    def initWindow(self):
        
        self.name_welcome_label = QLabel("尊敬的玩家，您好！\n")
        self.welcome_label = QLabel("欢迎使用LiquorDiceGame！,当前游戏暂未开始\n")
       
        # 创建按钮供用户选择两种游戏策略（ask）
        self.openButton = QPushButton("开")
        self.continueButton = QPushButton("继续猜测")
        self.openButton.setEnabled(False)
        self.continueButton.setEnabled(False)
       
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
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        # 设置窗口风格 大小图标
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('LiquorDiceGame')
        self.setWindowIcon(QIcon('./images/icon.png'))

   

    def update_gui(self,read_server_str,write_server):
        # # convert json's type to dict
        time.sleep(1)  # 延时2秒
        self.read_server_str=read_server_str
        self.write_server=write_server
        read_server_fn = json.loads(read_server_str)
        if read_server_fn['type'] == 'start_mesg':
            self.openButton.setEnabled(False)
            self.continueButton.setEnabled(False)
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
            if self.finish_decide is not True:
                self.type = 'Ask'
                self.openButton.setEnabled(True)
                self.continueButton.setEnabled(True)
                self.welcome_label.setText("\n当前轮到您的轮次，请从下面两个按钮中选择您要进行的操作")
                # 储存上一个用户的猜测
                self.last_num = read_server_fn['last_guess_num']
                self.last_face = read_server_fn['last_guess_face']
                self.last_zhai = read_server_fn['last_guess_zhai']
            if self.finish_decide is True:
                decide = {
                    'type': 'decide',
                    'num': self.num,  # 若为0则代表玩家选择开
                    'face': self.face,
                    'zhai': self.zhai
                }
                decide_mesg_json = json.dumps(decide)
                print(decide_mesg_json)
                write_server(decide_mesg_json)
                self.finish_decide = False
            
        elif read_server_fn['type'] == 's2c_decide':
            self.openButton.setEnabled(False)
            self.continueButton.setEnabled(False)
            self.type = 's2c_decide'
            self.player_id = read_server_fn['player_id'] # 广播用户id
            self.player_name = read_server_fn['player_name'] # 广播用户name
            self.num = read_server_fn['num'] # 广播用户猜测
            self.face = read_server_fn['face']
            self.zhai = read_server_fn['zhai']
            self.welcome_label.setText("现在"+str(self.player_id)+"号玩家"+str(self.player_name)+"的猜测结果是"+str(self.num)+str(self.face)+str(self.zhai)+"请您参考并等待进行下一步操作")
            
        elif read_server_fn['type'] == 'end':
            self.openButton.setEnabled(False)
            self.continueButton.setEnabled(False)
            self.type = 'end'
            self.dices = read_server_fn['dice'] # 最终结果
            self.names = read_server_fn['name'] # 最终玩家姓名
            self.info = read_server_fn['info']
            self.welcome_label.setText("游戏结束，各玩家的结果为"+str(self.dices)+"\n参与本轮游戏的玩家为"+str(self.names)) 
            self.name_welcome_label.setText(self.info)
                        

     # 该函数用于创建继续猜测的对话对象和读入用户输入
    def create_dialog(self):
        dialog = Dialog(self.last_num,self.last_face,self.last_zhai)
        result = dialog.exec_()  # 显示对话窗口并等待用户交互

        if result == QDialog.Accepted and dialog.get_user_input is not None:
            # 用户点击了对话窗口的“确定”按钮
            self.num,self.face,self.zhai = dialog.get_user_input()
            self.is_use_one=dialog.verify_use_one()
            self.finish_decide =  True
            self.update_gui(self.read_server_str,self.write_server)

    # 该函数用于处理开
    def open_action(self):
        self.finish_decide = True
        self.num = 0    




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
    if success_connect_str is not None:
        print('started!')
    thread = New_Thread(read_server=read_server,write_server=write_server)
    thread.finishSignal.connect(client.update_gui)
    thread.start()


    
    sys.exit(app.exec_())



if __name__ == '__main__':
    main_client()
    

