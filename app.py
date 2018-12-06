from flask import Flask, request, jsonify
import gghf.repository


app = Flask(__name__)
gghf.repository.db('desktop').create_index([('name', 'text')])


@app.route('/games')
def games():
    r = request.args
    limit = int(r.get('limit'))
    offset = int(r.get('offset'))
    platform = r.get('platform')
    store = r.get('store')
    region = r.get('region')

    sort_by = r.get('sort_by')
    genres = r.get('genres')
    _type = r.get('type')
    release_date = r.get('release_date')
    price = r.get('price')
    search = r.get('search')

    result = gghf.repository.query_games(
        sort_by, search, genres, _type, limit, offset, region, platform, store
    )
    return jsonify(result)