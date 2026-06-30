import sys
import subprocess
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class CeleryProcess:
    def __init__(self, command, cwd):
        self.command = command
        self.cwd = cwd
        self.process = None

    def start(self):
        self.stop()
        self.process = subprocess.Popen(self.command, cwd=self.cwd)

    def stop(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, celery_process):
        self.celery_process = celery_process
        self.last_restart = 0

    def on_any_event(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith('.py'):
            return
        if 'site-packages' in event.src_path or '__pycache__' in event.src_path:
            return
        now = time.time()
        if now - self.last_restart < 2:
            return
        self.last_restart = now
        self.celery_process.start()


class Command(BaseCommand):
    help = 'Run Celery worker with auto-reload on file changes'

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        cmd = [
            sys.executable, '-m', 'celery', '-A', 'config', 'worker',
            '-l', 'info', '-E',
        ]
        celery_process = CeleryProcess(cmd, str(base_dir))
        celery_process.start()

        handler = ChangeHandler(celery_process)
        observer = Observer()
        observer.schedule(handler, str(base_dir), recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            celery_process.stop()

        observer.join()
