# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import JsonResponse
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, Q
from elasticsearch_dsl.connections import connections
from rest_framework.decorators import api_view

import logging

logger = logging.getLogger(__name__)

connections.create_connection(hosts=[settings.ES_URL], timeout=20)

QUERIES = {
    'title': 'get_title',
    'speaker': 'get_speaker',
    'content': 'get_content',
}


def make_search():
    return Search(index=settings.ES_CW_INDEX)


def execute_search(query, sorting=None):
    search = make_search()
    if sorting:
        search = search.sort(sorting)
    results = search.query(query).execute()
    if results.success():
        return results
    return False


def get_speaker(name):
    return Match(speakers=name)


def get_title(title):
    return Match(title=title)


def get_content(content):
    return Q('match', content={'query': content, 'operator': 'and'})


@api_view(['GET'])
def search_by_speaker(request, name):
    """
    Search for a speaker by name
    :param request: 
    :param name: name of the congress person speaking
    :return: list sorted by date_issued
    """
    query = get_speaker(name)
    response = execute_search(query, '-date_issued')
    if response.success():
        return JsonResponse(response.to_dict())


@api_view(['GET'])
def search_by_title(request, title):
    """
    Search by title of a document
    :param request: 
    :param title: the title
    :return: list of results sorted by date_issued
    """
    query = get_title(title)
    response = execute_search(query, '-date_issued')
    if response.success():
        return JsonResponse(response.to_dict())


@api_view(['GET'])
def search_by_params(request):
    """
    Search by arbitrary params which can be combined
    
    title - search on the title field
    speaker - individual speakers
    content - search for text matches in the content add &highlight=<number> to include contextual
              matches of the given fragment size in the result (default is 200)
    
    Example: 
        http://127.0.0.1:8000/cwapi/search/multi/?speaker=schumer&content=trump&highlight=1000
    
    :param request: 
    :return: 
    """
    logger.debug("search_by_params")
    search = make_search().sort('-date_issued')
    params = request.query_params
    queries = []
    for f in QUERIES:
        if f in params:
            queries.append(globals()[QUERIES[f]](params[f]))
    logger.info("queries? %s " % queries)
    q = Q('bool', must=queries)

    if 'highlight' in params and 'content' in params:
        frag_size = params.get('highlight')
        if not frag_size.isnumeric():
            frag_size = 200
        response = search.highlight('content', fragment_size=frag_size).query(q).execute()
    else:
        response = search.query(q).execute()
    if response.success():
        return JsonResponse(response.to_dict())
    return JsonResponse("Found nothing")

