import pymongo
from gghf.repository import db


def make_query(sort_by, search, genres, _type):
    query = {'sort': [], 'find': {}}

    if search is not None:
        query['find']['$text'] = {'$search': search}

    if genres is not None:
        query['find']['genres'] = {'$in': genres.split(',')}

    if _type is not None:
        query['find']['type'] = {'$in': _type.split(',')}

    # sort_by format = sort_by=desc(name)
    if sort_by is not None:
        tokens = sort_by.split('(')
        key = tokens[0]
        value = pymongo.ASCENDING if tokens[1][:-1] == 'asc' else pymongo.DESCENDING
        query['sort'] = [(key, value)]
    else:
        query['sort'] = [('name', pymongo.DESCENDING)]

    return query


def query_games(sort_by, search, genres, _type, limit, offset, region, platform, store):
    query = make_query(sort_by, search, genres, _type)
    found = db(platform).find(query['find']).sort(query['sort']).limit(limit).skip(offset)

    result = []
    for game in found:
        game.pop('_id')
        prices = game.pop('price_latest')[store]
        region_price = next(filter(lambda x: x['region'] == region.upper(), prices), None)
        game['price'] = region_price
        result.append(game)

    return result
