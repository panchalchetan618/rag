import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Wait for database connection'

    def add_arguments(self, parser):
        parser.add_argument('--timeout', type=int, default=10)

    def handle(self, *args, **options):
        timeout = options['timeout']
        db_conn = connections['default']
        start = time.monotonic()
        while True:
            try:
                db_conn.ensure_connection()
                self.stdout.write(self.style.SUCCESS('Database available'))
                return
            except OperationalError:
                if time.monotonic() - start > timeout:
                    msg = f'Database unavailable after {timeout}s'
                    raise OperationalError(msg)
                self.stdout.write('Waiting for database...')
                time.sleep(1)
