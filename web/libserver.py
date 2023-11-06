import sys
import json
import socket
import functools
from PySide6.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget
from ldg_ui import Ui_Form
from PySide6.QtCore import QFile, QTextStream, QDate, Signal, Slot, Property, QThread
from PySide6.QtGui import QIntValidator


class ListenerThread(QThread):
    connect_signal = Signal(list)
    
    def __init__(self, host, port):
        super(ListenerThread, self).__init__()
        self.host = host
        self.port = port
        
    
    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print ('Listener thread started.')
        while True:
            client_socket, client_address = self.server_socket.accept()
            print('Connected')
            data = client_socket.recv(1024)
            if not data:
                continue
            name = data.decode('utf-8')
            print('Player', name, 'connected.')

            def write_fn(message):
                try:
                    # Send the message to the server
                    client_socket.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error occurred while sending message: {e}")

            def read_fn():
                try:
                    # Receive data from the server
                    data = client_socket.recv(1024)
                    # Decode the received data
                    message = data.decode('utf-8')
                    return message
                except Exception as e:
                    print(f"Error occurred while receiving message: {e}")
                    return None
            
            write_fn('Successfully connected to server.\n')
            self.client_socket = client_socket
            self.connect_signal.emit([name, read_fn, write_fn, client_socket])
            break
        self.server_socket.close()
        print('Listener thread finished.')
        


class Server(QWidget):
    def __init__(self, start_fn, host, port):
        super(Server, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.player_count = 0
        self.player_socket = []
        self.player_name = []
        self.player_read_fn = []
        self.player_write_fn = []
        self.setWindowTitle('服务器 ' + host + ':' + str(port))
        self.listener_thread = ListenerThread(host, port)
        self.listener_thread.connect_signal.connect(self.handle_client)
        
        player_num_validator = QIntValidator(1, 100)
        play_round_validator = QIntValidator(1, 100)
        self.ui.MaxPlayerEdit.setValidator(player_num_validator)
        self.ui.MaxPlayRoundEdit.setValidator(play_round_validator)
        self.ui.StartButton.clicked.connect(self.handle_start_button)
        self.ui.CloseButton.clicked.connect(self.handle_close_button)
        self.ui.MaxPlayerEdit.textChanged.connect(self.player_and_max_num_change_control)
        self.ui.DeletePlayerButton.clicked.connect(self.delete_chosen_player)
        self.ui.DisallowJump.setChecked(True)
        self.ui.DisallowZhai.setChecked(True)
        self.ui.MaxPlayerEdit.setText('8')
        self.ui.MaxPlayRoundEdit.setText('4')
        self.start_fn = start_fn
        self.listen_to_new_player()
        
        
    def listen_to_new_player(self):
        self.listener_thread.start()
        
    
    def player_and_max_num_change_control(self):
        max_num = self.get_max_player()
        if self.player_count > max_num:
            self.ui.StartButton.setEnabled(False)
        elif self.player_count == max_num:
            self.ui.StartButton.setEnabled(True)
        else:
            self.listen_to_new_player()
            self.ui.StartButton.setEnabled(True)
        
        
    def handle_client(self, client):
        name, read_fn, write_fn, client_socket = client
        self.player_count += 1
        self.player_socket.append(client_socket)
        self.player_name.append(name)
        self.player_read_fn.append(read_fn)
        self.player_write_fn.append(write_fn)
        self.ui.PlayerList.addItem(name)
        self.ui.PlayerList.setCurrentRow(self.player_count - 1)
        
        max_num = self.get_max_player()
        if self.player_count < max_num:
            self.listen_to_new_player()
        self.player_and_max_num_change_control()

        
        
    def delete_chosen_player(self):
        if self.player_count == 0:
            return
        index = self.ui.PlayerList.currentRow()
        if index == -1:
            return
        self.player_count -= 1
        player_socket = self.player_socket.pop(index)
        player_socket.close()
        self.player_name.pop(index)
        self.player_read_fn.pop(index)
        self.player_write_fn.pop(index)
        self.ui.PlayerList.takeItem(index)
        self.player_and_max_num_change_control()
        
        
    def handle_close_button(self):
        self.close()
        
        
    def get_max_round(self):
        max_round_str = self.ui.MaxPlayRoundEdit.text()
        if max_round_str == '':
            max_round = 4
        else:
            max_round = int(max_round_str)
        return max_round
    
    
    def get_max_player(self):
        max_player_str = self.ui.MaxPlayerEdit.text()
        if max_player_str == '':
            max_player = 1
        else:
            max_player = int(max_player_str)
        return max_player
        
    
    def handle_start_button(self):
        max_round = self.get_max_round()
        allow_zhai = self.ui.AllowZhai.isChecked()
        allow_jump = self.ui.AllowJump.isChecked()
        max_player = self.get_max_player()
        
        self.start_fn(
            self.player_name,
            self.player_read_fn,
            self.player_write_fn,
            max_player,
            max_round,
            allow_zhai,
            allow_jump,
            self.player_socket
        )
        

def game_logic_example(
    player_name,
    player_read_fn,
    player_write_fn,
    max_player_num,
    max_round,
    allow_zhai,
    allow_jump,
    player_socket
):
    print('game started')
    print('player name: ', player_name)
    print('player read fn: ', player_read_fn)
    print('player write fn: ', player_write_fn)
    print('max player num: ', max_player_num)
    print('max round: ', max_round)
    print('allow zhai: ', allow_zhai)
    print('allow jump: ', allow_jump)
    print('player socket: ', player_socket)
    
    
def start_server(start_fn, host, port):
    app = QApplication(sys.argv)

    window = Server(start_fn, host, port)
    window.show()

    sys.exit(app.exec())
    
        
if __name__ == "__main__":
    start_server(game_logic_example, '127.0.0.1', 12347)