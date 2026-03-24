import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class TestHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"Detected: {event.event_type} - {event.src_path}")

path = sys.argv[1] if len(sys.argv) > 1 else "."
observer = Observer()
observer.schedule(TestHandler(), path, recursive=True)
observer.start()
print(f"Watching {path} for changes... (Ctrl+C to stop)")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
