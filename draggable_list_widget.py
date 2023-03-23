from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QDrag, QCursor
from PyQt5.QtCore import Qt, QUrl, QMimeData, QPoint
import os
from PyQt5.QtWidgets import QFileIconProvider, QStyle, QListWidget, QApplication
from PyQt5.QtCore import QFileInfo
import shutil

class DraggableListWidget(QListWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            drag_distance = (event.pos() - self.drag_start_position).manhattanLength()
            if drag_distance >= QApplication.startDragDistance():
                drag = QDrag(self)
                mime_data = QMimeData()
                urls = []

                for item in self.selectedItems():
                    urls.append(QUrl.fromLocalFile(item.data(Qt.UserRole)))

                mime_data.setUrls(urls)
                drag.setMimeData(mime_data)

                drop_action = drag.exec_(Qt.CopyAction | Qt.MoveAction)

                if drop_action == Qt.MoveAction:
                    for item in self.selectedItems():
                        self.takeItem(self.row(item))
        else:
            super().mouseMoveEvent(event)




    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)


