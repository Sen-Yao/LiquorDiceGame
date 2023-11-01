# -*- coding: utf-8 -*-
import json
from PyQt5.QtCore import QThread, pyqtSignal

#定义一个线程类
class New_Thread(QThread):
    #自定义信号声明
    # 使用自定义信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    finishSignal = pyqtSignal(str,object)

    # 带一个参数t
    def __init__(self, read_server,write_server):
        super(New_Thread, self).__init__()
        self.read_server= read_server
        self.write_server = write_server

    #run函数是子线程中的操作，线程启动后开始执行
    def run(self):
        while True:
            read_server_str = self.read_server()
            #发射自定义信号
            #通过emit函数将参数i传递给主线程，触发自定义信号
            self.finishSignal.emit(read_server_str,self.write_server)  # 注意这里与_signal = pyqtSignal(str)中的类型相同
            