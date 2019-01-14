import requests
import json
import time
import gghf.parser.steam.game
import gghf.repository.games.update
import gghf.repository
import datetime
import watchdog.steamdog


def parse_game(game, appid):
    try:
        return gghf.parser.steam.game.from_steam(json.loads(game), appid)
    except Exception as ex:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_filename = '{0}_steam_info.txt'.format(now)
        with open(error_filename, 'w') as f:
            f.write(str(appid))
            f.write('\n')
            try:
                f.write(game)
            except Exception as ex:
                f.write('Cannot parse game\n')
                f.write(ex)
            f.flush()
        return None


def make_chunk(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def fetch_games_info(chunk, delay):
    games_prices = []
    update_operations = []

    for game in chunk:
        appid = str(game['appid'])
        url = 'https://store.steampowered.com/api/appdetails?appids={0}&cc=us'.format(
            appid)
        fetched = requests.get(url).text
        print('Fetched', appid)
        game = parse_game(fetched, appid)
        print('Parsed', appid)

        # something went bad and we need to check the error log!
        if game is None:
            time.sleep(delay)
            print('Game could not be parsed, look in the error logs', appid)
            continue

        # the game 'success' flag from steam is false
        if not game:
            time.sleep(delay)
            print('Steam returned success=False ', appid)
            continue

        # gghf supports only games and dlc's for now
        if game['type'] != 'game' and game['type'] != 'dlc':
            print('Is not game neither dlc, type is', game['type'])
            time.sleep(delay)
            continue

        # we assume if the game does not have US price, it is
        # not relevant to fetch prices for other countries
        fetched = json.loads(fetched)
        if fetched[appid]['data'].get('price_overview', None) is None:
            print('App probably is free, skipping price fetch', appid)
            update_operations.append(gghf.repository.games.update.make(game, [], 'steam'))
            time.sleep(delay)
            continue

        # if game was parsed and has price, add it to the games_prices
        # to fetch all prices in batch later
        games_prices.append(game)
        time.sleep(delay)

    return games_prices, update_operations


def scrap(all_games):
    # steam allows 200 request per 5 minutes, so delay 15 min between requests
    delay = 15
    # price overview appids count is max 100, so make an restriction
    rate_limit = 100

    for chunk in make_chunk(all_games, rate_limit):
        games_prices, update_operations = fetch_games_info(chunk, delay)

        print('Fetching prices for appids')
        appids = list(map(lambda x: str(x['appid']), games_prices))
        prices = watchdog.steamdog.fetch_prices(appids, delay)
        prices = watchdog.steamdog.parse_prices(prices, appids)

        # add the fetched price to model
        for game in games_prices:
            operation = gghf.repository.games.update.make(game, prices[str(game['appid'])], 'steam')
            update_operations.append(operation)

        gghf.repository.bulk_update('desktop', update_operations)
        print('Updated chunk')


def main():
    while True:
        # TODO: maybe add my real steam api key?
        all_games = requests.get(
            'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json').text
        all_games = json.loads(all_games)['applist']['apps']
        scrap(all_games)
