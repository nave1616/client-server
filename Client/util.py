from pathlib import Path
import pickle
import struct
from Files import *
import os
folder = os.path.dirname(os.path.realpath(__file__))
payload_size = struct.calcsize("i")
C = b'C'  # CACHE command
U = b'U'  # UPLOAD command
D = b'D'  # DOWNLOAD command

SERVER_PATH = Path(folder + '\\files')


def extract_meta(data):
    packed_size = data[:payload_size]
    command = data[payload_size:payload_size+1]
    msg_size = struct.unpack("i", packed_size)[0]
    return (msg_size, command)


def write_cache(data: pickle) -> None:
    with open(SERVER_PATH/'Cache.pic', 'wb') as writer:
        writer.write(data)


def read_cache() -> object:
    if not Path(SERVER_PATH/'cache.pic').exists():
        return pickle.loads(Folder(SERVER_PATH))
    with open(SERVER_PATH/'Cache.pic', 'rb') as reader:
        data = reader.read()
    return pickle.loads(data)


def write_file(name, data) -> None:
    with open(SERVER_PATH/name, 'wb') as writer:
        writer.write(data)


def read_file(path) -> None:
    if not Path(SERVER_PATH/path).exists:
        return None
    with open(SERVER_PATH/path, 'rb') as reader:
        data = reader.read()
    return data


def pack_object(object, cmd) -> bytes:
    data = pickle.dumps(object)
    message_size = struct.pack("i", len(data))
    return message_size + cmd + data


def unpack_object(data: pickle) -> object:
    return pickle.loads(data)
