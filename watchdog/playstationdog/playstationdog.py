# watchdog for playstation, uses playstation search and get API
# when fetch prices for american region, search game in other region and fetch price if exists

import gghf.parser.playstation.price
import requests
import json
import time

def fetch_prices(app, delay):
    prices = []

    # fetch prices for american region
    prices.extend(_scrap_prices(app['id'], american_region))
    
    # try to fetch prices for other regions
    for key, region in {'GB': european_region, 'HK': asian_region}.items():
        search_result = requests.get('https://store.playstation.com/store/api/chihiro/00_09_000/tumbler/{0}/en/999/{1}?suggested_size=100&mode=game'.format(key, app['name'])).text
        search_result = json.loads(search_result)['links']
        
        if search_result:
            game = next((x for x in list(search_result) if _compare(app, x)), None)
            
            if game is not None:
                print(game['id'])
                prices.extend(_scrap_prices(game['id'], region))

    time.sleep(delay)
    return prices


def parse_prices(prices, appid):
    parsed = []

    for region_price in prices:

        price = gghf.parser.playstation.price.from_playstation(region_price, appid)
        if price is not None:
            parsed.append(price)

    return parsed

def _scrap_prices(appid, regions):
    prices = []
    for region in regions:
        price_url = 'https://store.playstation.com/chihiro-api/viewfinder/{0}/{1}/999/{2}'.format(region[0], region[1], appid)
        
        print('GET', price_url)
        price = requests.get(price_url).json()
        
        price['region'] = region[0]
        prices.append(price)

    return prices

def _compare(game, fetched_game):
    return game['short_name'].lower() in fetched_game['short_name'].lower() and fetched_game['game_contentType'].lower() == game['game_contentType'].lower()



american_region = [
    ('US', 'en', 'STORE-MSF77008-ALLGAMES'),
    ('CA', 'en', 'STORE-MSF77008-ALLGAMES'),
    ('AR', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('BO', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('BR', 'pt', 'STORE-MSF77008-ALLGAMES'),
    ('CL', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('CO', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('CR', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('EC', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('SV', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('GT', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('HN', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('MX', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('NI', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('PA', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('PE', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('PY', 'es', 'STORE-MSF77008-ALLGAMES'),
    ('UY', 'es', 'STORE-MSF77008-ALLGAMES'),
]

european_region = [
    ('GB', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('KW', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('MT', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('OM', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('QA', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('SA', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('ZA', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('IT', 'it', 'STORE-MSF75508-FULLGAMES'),
    ('AU', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('IN', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('RU', 'ru', 'STORE-MSF75508-FULLGAMES'),
    ('UA', 'ru', 'STORE-MSF75508-FULLGAMES'),
    ('AT', 'de', 'STORE-MSF75508-FULLGAMES'),
    ('BE', 'fr', 'STORE-MSF75508-FULLGAMES'),
    ('BH', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('BG', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('HR', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('CY', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('CZ', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('DK', 'da', 'STORE-MSF75508-FULLGAMES'),
    ('FI', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('FR', 'fr', 'STORE-MSF75508-FULLGAMES'),
    ('DE', 'de', 'STORE-MSF75508-FULLGAMES'),
    ('GR', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('HU', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('IS', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('IE', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('IL', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('LU', 'fr', 'STORE-MSF75508-FULLGAMES'),
    ('NL', 'nl', 'STORE-MSF75508-FULLGAMES'),
    ('NZ', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('NO', 'no', 'STORE-MSF75508-FULLGAMES'),
    ('PL', 'pl', 'STORE-MSF75508-FULLGAMES'),
    ('PT', 'pt', 'STORE-MSF75508-FULLGAMES'),
    ('RO', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('SK', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('SI', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('ES', 'es', 'STORE-MSF75508-FULLGAMES'),
    ('SE', 'en', 'STORE-MSF75508-FULLGAMES'),
    ('CH', 'de', 'STORE-MSF75508-FULLGAMES'),
    ('TR', 'tr', 'STORE-MSF75508-FULLGAMES'),
    ('AE', 'en', 'STORE-MSF75508-FULLGAMES'),
]

asian_region = [
    ('ID', 'en', 'STORE-MSF86012-GAMESALL'),
    ('HK', 'en', 'STORE-MSF86012-GAMESALL'),
    ('KR', 'ko', 'STORE-MSF86012-GAMESALL'),
    ('MY', 'en', 'STORE-MSF86012-GAMESALL'),
    ('SG', 'en', 'STORE-MSF86012-GAMESALL'),
    ('TW', 'en', 'STORE-MSF86012-GAMESALL'),
    ('TH', 'en', 'STORE-MSF86012-GAMESALL'),
]