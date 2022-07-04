
# importing libraries
from mimetypes import init
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from Files import *
from pathlib import Path
from util import *
import shutil


class Window(QMainWindow):

    def __init__(self, sock, func):
        super().__init__()
        self.setWindowTitle("Cloud Files ")
        self.setGeometry(100, 100, 500, 400)
        tree = Tree(self, sock, func)
        tree.UiComponents()
        tree.load_folder()
        self.show()


class Tree(QTreeWidget):
    def __init__(self, parent, sock, upload):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.sock = sock
        self.upload = upload

        # Connect the contextmenu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menuContextTree)

    def UiComponents(self):
        '''Initialize geometry,columns,Labels of headers.'''
        width, height = self.parent_size()
        self.setGeometry(0, 0, width, height)
        self.setColumnCount(2)
        self.setHeaderLabels(["name", "size"])

    def parent_size(self):
        return self.parentWidget().frameGeometry().width(), self.parentWidget().frameGeometry().height()

    def load_folder(self):
        '''Load main files and folder to tree'''
        path = read_cache()
        for file in path.get_files():
            self.add_items(file, self)

    def add_items(self, file, Witem):
        '''add Subfolders/Files to tree'''
        item = QTreeWidgetItem(Witem, [file.get_name(), file.size_in_bytes()])
        item.setIcon(0, QIcon(file.icon_type()))
        if file.is_dir():
            for files in file.get_files():
                self.add_items(files, item)

    def dragEnterEvent(self, e) -> None:
        '''drag Enter Event Handler'''
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e) -> None:
        '''drag Move Event Handler
           accepted if drag object is url(file/folder)'''
        if e.mimeData().hasUrls():
            e.setDropAction(Qt.CopyAction)
            e.accept()

        else:
            e.ignore()

    def dropEvent(self, e) -> None:
        '''drop Event Handler, accepted if drop object is url(file/folder)
           add to tree on accepted'''
        if e.mimeData().hasUrls():
            e.setDropAction(Qt.CopyAction)
            e.accept()
            for url in e.mimeData().urls():
                url = init_path(url.toLocalFile())
                self.add_items(url, self)
            self.upload(self.sock, url)
        else:
            e.ignore()

    def menuContextTree(self, point):
        # Infos about the node selected.
        index = self.indexAt(point)

        if not index.isValid():
            return

        item = self.itemAt(point)
        # We build the menu.
        menu = QMenu()
        action_1 = menu.addAction("Download", self.download)

        menu.exec_(self.mapToGlobal(point))

    def download(self):
        path = self.getSelectedItem()
        pack = pack_object(path[0], b'U')
        self.sock.sendall(pack)

    def getSelectedItem(self):
        items = self.selectedItems()
        if len(items) == 0:
            return None
        item = items[0]
        return (item.data(0, Qt.DisplayRole), item.data(1, Qt.DisplayRole))


if __name__ == "__main__":
    pass
   # Application()
    # r'C:\Users\nave1\Desktop\demo'
