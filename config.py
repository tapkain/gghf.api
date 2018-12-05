import os


class Config:
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/gghfdb'
    MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE') or 'gghfdb'
    STEAM_API_KEY = os.environ.get('STEAM_API_KEY')
    FIREBASE_SERVER_KEY = os.environ.get('FIREBASE_SERVER_KEY')
    SLACK_API_KEY = os.environ.get('SLACK_API_KEY')
