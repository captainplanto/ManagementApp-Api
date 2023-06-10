# Django command to wait for database to start..
# from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("waiting for database to connect....")
        db_up = False
        while db_up:
            try:
                self.check(databases=["default"])
                db_up = True
            except ():
                self.stdout.write(
                    "Database unavailble, waiting 1 second.....")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("database available!"))
