from pathlib import Path


class abstract_file():
    def __init__(self, path):
        self.path = Path(path)
        self.name = self.path.name
        self.size = self.path.stat().st_size
        self.type = self.path.suffix

    def get_path(self) -> Path:
        '''return path of file/folder'''
        return self.path

    def get_name(self) -> str:
        '''return name of file/folder'''
        return self.name

    def is_dir(self) -> bool:
        '''return true if instance is dir'''
        return self.path.is_dir()

    def size_in_bytes(self) -> str:
        '''return size of file/folder in [B,KB,MB,GB,TB]'''
        size = self.get_size()
        i = 0
        Bytes = ["B", "KB", "MB", "GB", "TB"]
        while (size > 1024):
            size = size/1024
            i += 1
        return str(round(size, 2))+" "+Bytes[i]

    def get_size(self):
        '''return size of file/folder in bytes'''
        return self.size

    def get_type(self):
        '''return type of file/folder'''
        return self.type[1:]

    def icon_type(self):
        types = ["pdf", "folder", "png", "txt"]
        icon = self.get_type() if self.get_type() in types else "file"
        return "img\\"+icon + ".png"


class File(abstract_file):
    def __init__(self, path):
        super().__init__(path)
        self.icon = None

    def read_bytes(self):
        return self.path.read_bytes()


class Folder(abstract_file):
    def __init__(self, path):
        super().__init__(path)
        self.files = self.load_files(self.path)
        self.files_num = len(self.files)
        self.type = "folder"

    def get_type(self) -> str:
        '''override get_type func, return folder'''
        return self.type

    def num_of_files(self) -> int:
        '''return number of files in folder'''
        return self.files_num

    def find(self, file_name):
        for file in self.files:
            if file.get_name() == file_name:
                return file
        return None

    def get_size(self) -> int:
        '''override get_size func,return size of folder in bytes'''
        size = 0
        for file in self.files:
            size += file.get_size()
        return size

    def load_files(self, path) -> list:
        '''return list of files in folder'''
        files = []
        for file in path.iterdir():
            if file.is_dir():
                files.append(Folder(file))
            else:
                files.append(File(file))
        return files

    def get_files(self):
        '''return files/folder as objects'''
        return self.files

    def get_files_name(self) -> str:
        '''return name of files/folders'''
        names = []
        for file in self.files:
            if isinstance(file, Folder):
                names.append("D: " + file.get_name())
            else:
                names.append("F: " + file.get_name())
        return names


def init_path(path):
    return Folder(path) if Path(path).is_dir() else File(path)
