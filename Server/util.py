from asyncore import write
from pathlib import Path
import pickle
import struct
from Files import *
import os
payload_size = struct.calcsize("i")
C = b'C'  # CACHE command
U = b'U'  # UPLOAD command
D = b'D'  # DOWNLOAD command
folder = os.path.dirname(os.path.realpath(__file__))
USER_PATH = Path(folder + '\\files')


def extract_meta(data):
    packed_size = data[:payload_size]
    command = data[payload_size:payload_size+1]
    msg_size = struct.unpack("i", packed_size)[0]
    return (msg_size, command)


def write_cache(data: pickle) -> None:
    with open(USER_PATH/'Cache.pic', 'wb') as writer:
        writer.write(data)


def update_cache() -> object:
    data = pickle.dumps(Folder(USER_PATH))
    write_cache(data)


def read_cache() -> object:
    if not Path(USER_PATH/'cache.pic').exists():
        return pickle.loads(Folder(USER_PATH))
    with open(USER_PATH/'Cache.pic', 'rb') as reader:
        data = reader.read()
    return pickle.loads(data)


def write_file(name, data) -> None:
    with open(USER_PATH/name, 'wb') as writer:
        writer.write(data)


def read_file(path) -> None:
    if not Path(USER_PATH/path).exists:
        return None
    with open(USER_PATH/path, 'rb') as reader:
        data = reader.read()
    return data


def pack_object(object, cmd) -> bytes:
    data = pickle.dumps(object)
    message_size = struct.pack("i", len(data))
    return message_size + cmd + data


def unpack_object(data: pickle) -> object:
    return pickle.loads(data)
