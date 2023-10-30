import socket
import functools


# usage:
# send message to server: write_fn('message')
# listen from server: message = read_fn()
def get_remote_fn(server_ip, server_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_port))
    reader, writer = s.makefile('rb'), s.makefile('wb')
    read_fn = functools.partial(read, reader)
    write_fn = functools.partial(write, writer)
    return read_fn, write_fn


def read(reader):
    return reader.readline().decode().strip()


def write(writer, message):
    writer.write(message.encode())
    writer.flush()