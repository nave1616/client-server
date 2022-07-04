import socket
from threading import Thread
from util import *
from Tree import *

HOST = 'localhost'
PORT = 50007
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def get_msg(conn):
    while True:
        packed = conn.recv(5)
        buffer, cmd = extract_meta(packed)
        data = handle_msg(conn, buffer)  # Server send last cache
        if cmd == C:
            write_cache(data)
        # Server upload/Client download (data contain pickle info)
        if cmd == D:
            file = unpack_object(data)
            file_name = file.get_name()
            buffer = file.get_size()
            file_handler(conn, file_name, buffer)


def file_handler(conn, file_name, buffer):
    data = handle_msg(conn, buffer)
    write_file(file_name, data)


def handle_msg(conn, buffer) -> bytes:
    data = b''
    while 1024 < buffer:
        data += conn.recv(1024)
        buffer -= 1024
    data += conn.recv(buffer)
    return data


def upload(conn, file_obj):
    data = pack_object(file_obj, b"D")
    conn.sendall(data)  # first msg File data
    data = file_obj.read_bytes()  # second msg binary data
    conn.sendall(data)


def Application(sock, func):
    '''Create main window'''
    App = QApplication(sys.argv)
    App.setObjectName("Cloud")
    window = Window(sock, func)
    sys.exit(App.exec())


if __name__ == "__main__":
    msg = Thread(target=get_msg, args=(sock,))
    msg.setDaemon(True)
    msg.start()
    Application(sock, upload)

    sock.close()
