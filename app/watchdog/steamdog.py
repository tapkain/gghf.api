# watchdog for steam, uses steam PICS update API
# when app has received updates, fetch price and news for the app

from gevent import monkey
monkey.patch_all()
from steam.client import SteamClient
from steam.enums import EResult
import requests
from pymongo import UpdateOne
from app.parser.price import PriceParser


delay = 15
steam = SteamClient()
test_regions = [
    'US', 'AR'
]
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
def fetch_prices(apps):
    prices = []
    appids = ','.join(list(map(lambda x: str(x.appid), apps)))
    print('Apps to change -', appids)

    for region in test_regions:
        price_url = 'https://store.steampowered.com/api/appdetails?appids={0}&cc={0}&filters=price_overview'.format(
                appids, region)
        print('Fetching price for {0} region'.format(region))
        prices.append(requests.get(price_url).json())
        prices['region'] = region
        steam.sleep(15)

    return price

def make_updates(prices, apps):
    updates = []

    for region_price in prices:
        for app in apps:
            price = region_price.get(app.appid, None)
            if price is None or not price['success']:
                continue
            price = price['data']
            price['region'] = region_price['region']
            price = PriceParser.from_steam(price)
            print(price)
            updates.append(UpdateOne({'_id': app.appid}, {'$set': {'price': price}}, upsert=True))

    return updates


def main():
    if steam.anonymous_login() == EResult.Fail:
        print('Cannot login anonymously to steam')
        return

    payload = steam.get_changes_since(0)
    current_change_number = payload.current_change_number

    while True:
        payload = steam.get_changes_since(current_change_number)
        
        if len(payload.app_changes) != 0:
            for price in fetch_prices(payload.app_changes):
                print(price)

        current_change_number = payload.current_change_number
        print('Change number: ', current_change_number)
        steam.sleep(delay)

if __name__ == '__main__':
    main()