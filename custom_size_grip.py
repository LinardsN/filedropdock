# custom_size_grip.py
from PyQt5.QtWidgets import QSizeGrip
from PyQt5.QtCore import Qt, QSize

from PyQt5.QtWidgets import QSizeGrip
from PyQt5.QtCore import Qt, QSize

class CustomSizeGrip(QSizeGrip):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()
            self.startSize = self.window().size()
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            delta = event.pos() - self.startPos
            newSize = QSize(self.startSize.width() + delta.x(), self.startSize.height() + delta.y())
            self.window().resize(newSize)
            event.accept()
        else:
            event.ignore()


