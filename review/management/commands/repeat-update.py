from django.core.management.base import BaseCommand
from . import updatereview
from rq import Queue
from rq_scheduler import Scheduler
from datetime import timedelta, datetime
import redis


def job():
    print(datetime.now())


class Command(BaseCommand):



    def handle(self, *args, **options):

        scheduler = Scheduler(connection=redis.Redis())
        # scheduler.enqueue_at(datetime.now(), job())
        com = updatereview.Command()
        scheduler.cron(
            '* * * * *',  # Time for first execution, in UTC timezone
            func=job,

        )