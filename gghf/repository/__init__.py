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

from gghf.repository.query_games import query_games
