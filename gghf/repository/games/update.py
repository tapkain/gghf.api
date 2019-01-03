from pymongo import UpdateOne


def make(game, prices, source):
    game['price_latest'] = {source: prices}
    return UpdateOne({'appid': game['appid']}, {'$set': game}, upsert=True)


