import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QListWidgetItem
from PyQt5.QtCore import QTimer, QMimeData, Qt
from PyQt5.QtGui import QClipboard

class ClipboardHistoryWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # self.label = QLabel('Clipboard History')
        # layout.addWidget(self.label)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.clipboard_data_changed)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_clipboard)

        self.old_clipboard_text = self.clipboard.text()

        # Connect the itemSelectionChanged signal to the copy_selected_item function
        self.list_widget.itemSelectionChanged.connect(self.copy_selected_item)

    def clipboard_data_changed(self):
        text = self.clipboard.text().strip()
        if text and text != self.old_clipboard_text:
            self.timer.start(500)
            return

        if not text:
            return

        # Check if the item is already in the list_widget
        for item in self.list_widget.findItems(text[:25], Qt.MatchStartsWith): # Changed Qt.MatchExactly to Qt.MatchStartsWith
            if text == item.data(Qt.UserRole): # Check if the full text matches
                return

        item = QListWidgetItem(text[:25] + "..." if len(text) > 25 else text)
        item.setData(Qt.UserRole, text)  # Store the full text in the item
        self.list_widget.insertItem(0, item)
        self.old_clipboard_text = text


    def clear(self):
        self.list_widget.clear()

    def copy_selected_item(self):
        item = self.list_widget.currentItem()
        if item:
            full_text = item.data(Qt.UserRole)  # Retrieve the full text from the item
            if self.clipboard.text() != full_text:  # Check if the text is not already in the clipboard
                self.timer.stop()  # Stop the timer to avoid duplicates
                self.clipboard.blockSignals(True)
                self.clipboard.setText(full_text)
                self.clipboard.blockSignals(False)
                self.timer.start(500)  # Start the timer again after copying

    # Update the check_clipboard function
    def check_clipboard(self):
        current_text = self.clipboard.text()
        if current_text != self.old_clipboard_text:
            self.old_clipboard_text = current_text
            self.clipboard_data_changed()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clipboard_history_widget = ClipboardHistoryWidget()
    clipboard_history_widget.show()
    sys.exit(app.exec_())

