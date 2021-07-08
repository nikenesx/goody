from django.core.management.base import BaseCommand
from review.models import Review
import logging


class Command(BaseCommand):

    def handle(self):
        formatter = logging.Formatter("[%(asctime)s]: %(message)s")
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler('/home/gritsanenko/Рабочий стол/Задание/app/debug.log')
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.info('Command updatereview started.')
        reviews = Review.objects.all()
        logger.info('%s reviews will be updated.', reviews.count())
        count = 0
        for rev in reviews:
            rev.processed_rev_text = rev.remake_rev()
            rev.save()
            count += 1

        logger.info('%s reviews has been updated successfully.', count)
        logger.info('Command updatereview ended.')
