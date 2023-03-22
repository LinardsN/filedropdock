import sys
import os
import shutil
import mimetypes
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QShortcut,
                             QListWidget, QListWidgetItem, QAbstractItemView, QGraphicsBlurEffect, QGroupBox, QSizeGrip, QCheckBox)
from PyQt5.QtCore import Qt, QUrl, QPoint, QMimeData, QSize, QEvent
from PyQt5.QtGui import QIcon, QKeySequence, QDrag
from draggable_list_widget import DraggableListWidget
from clipboard_history_widget import ClipboardHistoryWidget
from custom_size_grip import CustomSizeGrip

class DockOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dock Overlay')
        self.setGeometry(100, 100, 300, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        # Clipboard History Widget
        clipboard_history_group = QGroupBox("Clipboard History")
        clipboard_history_layout = QVBoxLayout()
        clipboard_history_layout.setContentsMargins(1, 10, 1, 1)  # Set the margins (left, top, right, bottom)
        self.clipboard_history_widget = ClipboardHistoryWidget()
        clipboard_history_layout.addWidget(self.clipboard_history_widget)
        clipboard_history_group.setLayout(clipboard_history_layout)
        layout.addWidget(clipboard_history_group)


        # Draggable File List Widget
        draggable_file_list_group = QGroupBox("Draggable File List")
        draggable_file_list_layout = QVBoxLayout()
        draggable_file_list_layout.setContentsMargins(10, 20, 10, 10)  # Set the margins (left, top, right, bottom)
        self.list_widget = DraggableListWidget(self)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setDragDropMode(QAbstractItemView.DragOnly)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setViewMode(QListWidget.IconMode)  # Set view mode to IconMode
        self.list_widget.setIconSize(QSize(64, 64))  # Set icon size
        self.list_widget.setMinimumHeight(100)  # Add a minimum height
        draggable_file_list_layout.addWidget(self.list_widget)

        self.copy_mode_checkbox = QCheckBox("Copy Mode")
        draggable_file_list_layout.addWidget(self.copy_mode_checkbox)

        draggable_file_list_group.setLayout(draggable_file_list_layout)
        layout.addWidget(draggable_file_list_group)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Resize overlay
        self.size_grip = CustomSizeGrip(self)
        self.size_grip.setFixedSize(15, 15)
        self.size_grip.move(self.width() - self.size_grip.width(), self.height() - self.size_grip.height())
        self.size_grip.raise_()

        self.setMouseTracking(True)
        self.drag_start_position = None

        # Install event filter for child widgets
        self.clipboard_history_widget.list_widget.viewport().installEventFilter(self)  # Corrected line
        self.list_widget.viewport().installEventFilter(self)

        # Load styles from the styles.qss file
        with open("styles.qss", "r") as file:
            self.setStyleSheet(file.read())

    def eventFilter(self, obj, event):
        if obj == self.clipboard_history_widget.list_widget.viewport() or obj == self.list_widget.viewport():
            if event.type() == QEvent.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                    return True
            elif event.type() == QEvent.Drop:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()

                    if self.copy_mode_checkbox.isChecked():
                        event.setDropAction(Qt.CopyAction)
                    else:
                        event.setDropAction(Qt.MoveAction)
                    return True
        return super().eventFilter(obj, event)

    def eventFilter(self, obj, event):
        if obj == self.clipboard_history_widget.list_widget.viewport() or obj == self.list_widget:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
                return True
            elif event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton:
                if self.drag_start_position is not None:
                    self.move(event.globalPos() - self.drag_start_position)
                    return True
        return super().eventFilter(obj, event)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()
        else:
            event.ignore()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update the position of the size grip when the window is resized
        self.size_grip.move(self.width() - self.size_grip.width(), self.height() - self.size_grip.height())

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            print(f'Dropped file: {file_path}')

            file_name = os.path.basename(file_path)

            # Add the dropped file to the list widget
            item = QListWidgetItem(file_name)
            item.setData(Qt.UserRole, file_path)  # Store the file path in the item

            # Set the icon according to mime type
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('video'):
                item.setIcon(QIcon("video_icon.png"))
            else:
                item.setIcon(QIcon(file_path))

            self.list_widget.addItem(item)

def run_overlay():
    app = QApplication(sys.argv)
    overlay = DockOverlay()
    overlay.show()
    sys.exit(app.exec_())
