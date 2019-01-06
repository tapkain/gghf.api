import requests
import json
import gghf.parser.playstation.game 
import gghf.parser.playstation.price 
import os
import datetime
import watchdog.playstationdog

def parse_game(game):
    return gghf.parser.playstation.game.from_playstation(game)

def scrap(all_games):
    # playstation contains approximately 4000 games and price must be updated every day, so delay 10 sec between different games
    delay = 15
    
    update_operations = []
    for item in all_games:
        
        game = parse_game(item)
        
        prices = watchdog.playstationdog.fetch_prices(item, delay)
        prices = watchdog.playstationdog.parse_prices(prices, game['appid'])
 
        if prices is None or not prices:
            print('App probably is free, skipping price fetch', game['appid'])
            update_operations.append(gghf.repository.games.update.make(game, [], 'playstation'))
            continue

        operation = gghf.repository.games.update.make(game, prices, 'playstation')
        update_operations.append(operation)

        gghf.repository.bulk_update('playstation', update_operations)
        print('Updated chunk')

def main():
    offset = 0
    amount = 99
    while True:
        all_games = []
        while True:
            # use pagination to get all games
            games = requests.get('https://store.playstation.com/chihiro-api/viewfinder/US/en/999/STORE-MSF77008-ALLGAMES?start={0}&size={1}&gameContentType=games'.format(offset, amount)).text
            games = json.loads(games)['links']
            if not games:
                break

            all_games.extend(games)
            offset += amount

        scrap(all_games)
        
                    

