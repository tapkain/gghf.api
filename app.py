from flask import Flask, request, jsonify
from pymongo import MongoClient, UpdateOne
import pymongo
from config import Config


app = Flask(__name__)
mongo = MongoClient(Config.MONGODB_URI)
db_name = Config.MONGODB_DATABASE
mongo[db_name].desktop_games.create_index([('name', 'text')])


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


@app.route('/games')
def games():
    r = request.args
    limit = int(r.get('limit'))
    offset = int(r.get('offset'))
    platform = r.get('platform')

    sort_by = r.get('sort_by')
    genres = r.get('genres')
    _type = r.get('type')
    release_date = r.get('release_date')
    price = r.get('price')
    search = r.get('search')
    query = make_query(sort_by, search, genres, _type)
    found = mongo[db_name].desktop_games.find(query['find']).sort(query['sort']).limit(limit).skip(offset)
    result = []

    for game in found:
        game.pop('_id')
        result.append(game)

    return jsonify(result)