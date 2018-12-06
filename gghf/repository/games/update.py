from pymongo import UpdateOne


def make(game, prices):
    game['price_latest'] = {'steam': prices}
    return UpdateOne({'appid': game['appid']}, {'$set': game}, upsert=True)


