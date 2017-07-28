from django_extensions.management.jobs import DailyJob
from interesting.models import *
import logging

logger = logging.getLogger(__name__)


class Job(DailyJob):
    help = "Fetch the daily interesting data"

    def execute(self):
        topics = InterestingSearch.objects.all()
        for topic in topics:
            logging.info("topic: {}".format(topic.name))
