# watchdog for steam, uses steam PICS update API
# when app has received updates, fetch price and news for the app

from gevent import monkey
monkey.patch_all()
from steam.client import SteamClient
from steam.enums import EResult
import requests
from pymongo import UpdateOne
from watchdog.steamdog.parser import PriceParser

delay = 15
steam = SteamClient()
supported_regions = [
    'US', 'AR', 'TR', 'RU', 'KZ', 'IN',
    'ID', 'VN', 'TH', 'PH', 'BR', 'CO',
    'ZA', 'MY', 'MX', 'SA', 'UA', 'TW',
    'PE', 'KW', 'QA', 'CL', 'HK', 'UY',
    'SG', 'CR', 'AE', 'NO', 'NZ', 'CA',
    'JP', 'KR', 'EURO', 'PL', 'GB', 'CN',
    'IL', 'CH', 'AU'
]

# fetch prices for all apps from supported regions
def fetch_prices(apps, regions=supported_regions, delay=delay):
    prices = []
    appids = ','.join(list(map(lambda x: str(x.appid), apps)))
    print('Apps to change -', appids)

    for region in regions:
        # TODO: there could be an edge case then we are fetching price for more than 100 apps
        price_url = 'https://store.steampowered.com/api/appdetails?appids={0}&cc={1}&filters=price_overview'.format(
                appids, region)
        print('GET', price_url)
        price = requests.get(price_url).json()
        price['region'] = region
        prices.append(price)
        steam.sleep(15)

    return prices

# make db-ready collection from steam input
def parse_prices(prices, apps):
    parsed = []

    for region_price in prices:
        for app in apps:
            price = PriceParser.from_steam(region_price, str(app.appid))
            if price is not None:
                parsed.append(price)

    return parsed

def main(change_number=0):
    if steam.anonymous_login() == EResult.Fail:
        print('Cannot login anonymously to steam')
        return

    payload = steam.get_changes_since(change_number)
    current_change_number = payload.current_change_number

    while True:
        payload = steam.get_changes_since(current_change_number)
        
        if len(payload.app_changes) != 0:
            prices = fetch_prices(payload.app_changes)
            updates = make_price_updates(prices, payload.app_changes)

        current_change_number = payload.current_change_number
        print('Change number: ', current_change_number)
        steam.sleep(delay)