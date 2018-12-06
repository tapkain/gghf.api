from config import Config
import pymongo
from pymongo import MongoClient


mongo = MongoClient(Config.MONGODB_URI)
db_name = Config.MONGODB_DATABASE


def db(platform):
    if platform == 'desktop':
        return mongo[db_name].desktop_games
    else:
        # return by now always desktop games
        return mongo[db_name].desktop_games


def bulk_update(platform, updates):
    try:
        db(platform).bulk_write(updates)
    except Exception as ex:
        print('Bulk update error', ex)
        
