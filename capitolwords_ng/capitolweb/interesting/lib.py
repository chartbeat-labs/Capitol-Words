import logging
from interesting.models import *
from datetime import timedelta
from datetime import datetime
from cwapi.views import make_search, get_entity, get_content
from elasticsearch_dsl.query import Q, Range
from django.db import IntegrityError
import pprint

logger = logging.getLogger(__name__)


def format_date(d):
    return d.strftime('%Y-%m-%d')


def format_result_date(d):
    return datetime.strptime(d, '%Y-%m-%dT%H:%M:%S')


def find_interesting(topic, start_date, days_forward=1):
    """
    Takes a topic and a day and finds any matching docs
    :param topic: an InterestingSearch object
    :param start_date: a datetime day
    :param days_forward: # of days forward, non-inclusive. Leaving this with default 1 gives you 1 days worth of data.
    :return: a scanner over the results
    """

    # get results searching for namedentities
    logger.info("searching on %s", topic)

    # date range should be one full day
    end_date = start_date + timedelta(days=days_forward)

    must_queries = []
    must_queries.append(Q('range', date_issued={"gte": format_date(start_date), "lt": format_date(end_date)}))
    [must_queries.append(get_content(e.entity)) for e in topic.entities.all()]
    logger.info(must_queries)
    # we restrict to the range but look for potentially multiple named entities
    q = Q('bool', must=must_queries)
    logger.info(q)
    results = make_search().params(track_scores=True).highlight('content', fragment_size=500).query().scan()
    return results


def get_speaker_for_name(name):
    try:
        return CongressPerson.objects.get(official_full=name)
    except Exception:
        logger.warning("Could not find speaker %s", name)
        return None


def process_hit(topic, hit):
    logger.info("Processing next hit for %s - %s", topic.name, hit.meta.score)
    if hit.speakers:
        document_id = hit.ID
        document_date = format_result_date(hit.date_issued)
        document_title = hit.title
        document_score = hit.meta.score
        fragment = hit.hightlight.content if 'highlight' in hit else None

        for speaker in hit.speakers:
            speaker_obj = get_speaker_for_name(speaker)
            if speaker_obj:
                result = FoundResult(interesting_search=topic, speaker=speaker_obj, document_id=document_id,
                                     document_date=document_date, document_title=document_title, score=document_score)
                if fragment:
                    result.fragment = hit.hightlight.content
                try:
                    result.save()
                except IntegrityError:
                    logger.warn("Got a duplicate result %s ", result)
    else:
        logger.warn("No speakers for hit: %s", hit)




