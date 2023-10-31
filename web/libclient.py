import socket

# usage:
# send message to server: write_fn('message')
# listen from server: message = read_fn()
def get_remote_fn(server_ip, server_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_port))
    
    def write_fn(message):
        try:
            # Send the message to the server
            s.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error occurred while sending message: {e}")

    def read_fn():
        try:
            # Receive data from the server
            data = s.recv(1024)
            # Decode the received data
            message = data.decode('utf-8')
            return message
        except Exception as e:
            print(f"Error occurred while receiving message: {e}")
            return None
    
    # Return the functions for writing and reading from the server
    return read_fn, write_fn


if __name__ == '__main__':
    read_fn, write_fn = get_remote_fn('127.0.0.1', 12347)
    write_fn('hello')
    print("write")
    print(read_fn())