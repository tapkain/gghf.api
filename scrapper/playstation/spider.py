import requests
import json
import gghf.parser.playstation.game 
import gghf.parser.playstation.price 
import os
import datetime
import watchdog.playstationdog

import logging
import logging.handlers as handlers
import time
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('logger')

def parse_game(game):
    try:
        return gghf.parser.playstation.game.from_playstation(game)
    except Exception:
        logger.exception('Cannot parse game {0}'.format(game.get('id', '')))
        return None
    

def scrap(all_games):
    
    # playstation contains approximately 4000 games and price must be updated every day, so delay 10 sec between different games
    delay = 15
    
    update_operations = []
    for item in all_games:
        game = parse_game(item)
        logger.info('Parsed {0}'.format(game['appid']))
        
        # something went bad and we need to check the error log!
        if game is None:
            logger.warn('Game could not be parsed, look in the error logs {0}'.format(game['appid']))
            continue

        prices = watchdog.playstationdog.fetch_prices(item, delay)
        prices = watchdog.playstationdog.parse_prices(prices, game['appid'])
 
        # we assume if the game does not have US price, it is
        # not relevant to fetch prices for other countries
        if prices is None or not prices:
            logger.warn('App probably is free, skipping price fetch {0}'.format(game['appid']))
            update_operations.append(gghf.repository.games.update.make(game, [], 'playstation'))
        else:
            operation = gghf.repository.games.update.make(game, prices, 'playstation')
            update_operations.append(operation)

        gghf.repository.bulk_update('playstation', update_operations)
        logger.info('Updated chunk')

def main():
    offset = 0
    amount = 99
    while True:
        all_games = []
        logger.info('Start scrap playstation games')
        while True:
            # use pagination to get all games
            try:
                games = requests.get('https://store.playstation.com/chihiro-api/viewfinder/US/en/999/STORE-MSF77008-ALLGAMES?start={0}&size={1}&gameContentType=games'.format(offset, amount)).text
                games = json.loads(games)['links']
            except Exception:
                games = None
                logger.exception('Cannot load page {0}'.format(offset/amount + 1))
                continue
            finally:
                offset += amount

            if not games:
                break

            all_games.extend(games)
            
        logger.info('Finish scrap games, {0} pages'.format(offset/amount + 1))
        scrap(all_games)
        
                    

