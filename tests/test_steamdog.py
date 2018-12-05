import watchdog.steamdog
import json

class TestApp:
    def __init__(self, appid):
        self.appid = appid

prices = None
test_app_changes = [TestApp(730), TestApp(65540)]
test_regions = ['US', 'AR']

def test_fetch_prices():
    prices = watchdog.steamdog.fetch_prices(test_app_changes, test_regions, 0)

def test_parse_prices():
    with open('tests/steam_prices.json', 'r') as f:
        prices = json.loads(f.read())
        parsed = watchdog.steamdog.parse_prices(prices, test_app_changes)
        
        with open('tests/db_prices.json', 'r') as db:
            db_prices = json.loads(db.read())
            assert len(parsed) == len(db_prices)

            for p in zip(parsed, db_prices):
                assert p[0]['store'] == p[1]['store']
                assert p[0]['region'] == p[1]['region']
                assert p[0]['initial'] == p[1]['initial']
                assert p[0]['currency'] == p[1]['currency']