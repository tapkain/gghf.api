# watchdog for steam, uses steam PICS update API
# when app has received updates, fetch price and news for the app

import gghf.parser.steam.price
import requests
from steam.enums import EResult
from steam.client import SteamClient

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


def fetch_prices(apps, delay=delay, regions=supported_regions):
    # fetch prices for all apps from supported regions
    prices = []

    if len(apps) == 0:
        print('No apps to fetch price for')
        return prices

    appids = ','.join(apps)
    print('Apps to change -', appids)

    for region in regions:
        # TODO: there could be an edge case then we are fetching price for more than 100 apps
        price_url = 'https://store.steampowered.com/api/appdetails?appids={0}&cc={1}&filters=price_overview'.format(
            appids, region)
        print('GET', price_url)
        price = requests.get(price_url).json()
        price['region'] = region
        prices.append(price)
        steam.sleep(delay)

    return prices


def parse_prices(prices, apps):
    # make db-ready collection from steam input
    parsed = {}
    for appid in apps:
        parsed[appid] = []

    for region_price in prices:
        for appid in apps:
            price = gghf.parser.steam.price.from_steam(region_price, appid)
            if price is not None:
                parsed[appid].append(price)

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
            apps = list(map(lambda x: str(x.appid), payload.app_changes))
            prices = fetch_prices(apps)
            updates = make_price_updates(prices, apps)

        current_change_number = payload.current_change_number
        print('Change number: ', current_change_number)
        steam.sleep(delay)
