# Clipboard History and Draggable File List Dock Overlay

This is a simple PyQt5-based application that provides a Clipboard History widget and a Draggable File List widget. The application is designed to stay on top of other windows, allowing you to quickly access your clipboard history and files.

## Features
### Clipboard History widget: 
Displays a list of recent clipboard text entries, allowing you to easily copy them back to the clipboard by selecting the desired entry.
### Draggable File List widget: 
Displays a list of files that can be dragged into other applications. Users can choose between copy mode and move mode.
### Customizable window: 
The application window can be resized and moved easily.
### Requirements:
Python 3.6+
PyQt5

### To install PyQt5, run the following command:
```bash
pip install PyQt5
```

## Usage
To run the application, execute the following command from the terminal:
```bash
python main.py
```

The application window will appear, displaying the Clipboard History widget and the Draggable File List widget.

## Clipboard History Widget
Whenever you copy text to the clipboard, the text will automatically appear at the top of the Clipboard History widget. To copy an item from the list back to the clipboard, simply select the item in the list. To clear the clipboard history, click the "Clear" button.

## Draggable File List Widget
To add files to the Draggable File List widget, drag and drop them onto the widget. The files will be displayed with their respective icons. To drag a file from the list into another application, click and drag the file from the list. To toggle between copy mode and move mode, check or uncheck the "Copy Mode" checkbox.

## Customization
The appearance of the application can be customized by modifying the styles.qss file. This file contains the stylesheet for the application's UI components. To change the appearance of a specific UI component, simply update the corresponding CSS properties in the styles.qss file.
