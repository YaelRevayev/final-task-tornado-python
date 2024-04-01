import time
import threading
from logger import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_files import classifyFiles

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filename = event.src_path
        logger.info(f"New file detected: {filename}")
        threading.Thread(target=classifyFiles,args=(filename,)).start()

def start_watchdog(directory):
    observer = Observer()
    observer.schedule(NewFileHandler(), directory, recursive=True)
    observer.start()
    logger.info(f"Watching directory: {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

