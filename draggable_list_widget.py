from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QDrag, QCursor
from PyQt5.QtCore import Qt, QUrl, QMimeData, QPoint
import os
from PyQt5.QtWidgets import QFileIconProvider, QStyle, QListWidget
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

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            icon_provider = QFileIconProvider()
            for url in urls:
                local_file_path = url.toLocalFile()
                item = QListWidgetItem(url.fileName())
                item.setToolTip(local_file_path)
                item.setData(Qt.UserRole, local_file_path)
                file_info = QFileInfo(local_file_path)
                file_icon = icon_provider.icon(file_info)
                item.setIcon(file_icon)
                self.addItem(item)

            event.acceptProposedAction()

    def startDrag(self, supportedActions):
        items = self.selectedItems()
        drag = QDrag(self)
        mime_data = QMimeData()
        urls = []

        for item in items:
            urls.append(QUrl.fromLocalFile(item.data(Qt.UserRole)))

        mime_data.setUrls(urls)
        drag.setMimeData(mime_data)

        default_action = Qt.MoveAction if not self.main_window.copy_mode_checkbox.isChecked() else Qt.CopyAction
        result = drag.exec_(supportedActions, default_action)

        for item in items:
            self.takeItem(self.row(item))

