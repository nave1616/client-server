import socket
from threading import Thread, Semaphore
from util import *
from Files import *
import os
FILES_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '\\files'
CACHE = Folder(FILES_FOLDER)
HOST = 'localhost'
PORT = 50007
LOCK = Semaphore(0)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()


def get_msg(conn):
    while True:
        try:
            packed = conn.recv(5)
            buffer, cmd = extract_meta(packed)
            data = handle_msg(conn, buffer)  # return data in bytes
            file = unpack_object(data)
            if cmd == D:
                file_handler(conn, file.get_name(), file.get_size())
            if cmd == U:
                upload(conn, file)
        except:
            conn.close()


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


def upload(conn, file_name):
    file = CACHE.find(file_name)
    data = pack_object(file, b"D")
    conn.sendall(data)  # first msg File data
    data = file.read_bytes()  # second msg binary data
    conn.sendall(data)


conn, addr = sock.accept()
conn.sendall(pack_object(CACHE, C))  # SEND SERVER FILES
user = Thread(target=get_msg, args=(conn,))
# user.setDaemon = True
user.start()
user.join()
sock.close()
