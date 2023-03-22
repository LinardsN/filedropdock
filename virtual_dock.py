from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, shutil, os

class DockHandler(FileSystemEventHandler):
    def __init__(self, file_map):
        self.file_map = file_map

    def on_created(self, event):
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)
        self.file_map[filename] = event.src_path
        print(f'File added to dock: {filename}')

    def on_deleted(self, event):
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)
        if filename not in self.file_map:
            return

        src_path = self.file_map[filename]
        dest_path = os.path.join(os.path.dirname(event.src_path), filename)

        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f'File copied from {src_path} to {dest_path}')
        else:
            print(f'Source file not found: {src_path}')

        del self.file_map[filename]

def monitor_dock():
    file_map = {}
    dock_handler = DockHandler(file_map)
    observer = Observer()
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    monitor_dock()
