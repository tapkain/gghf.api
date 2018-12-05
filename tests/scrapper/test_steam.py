from scrapper.steam.spider import parse_game
import json

def test_parse_game():
    with open('tests/scrapper/steam_games.json', 'r') as f:
        payload = f.read()
        parsed = parse_game(payload, 730)

        with open('tests/scrapper/db_games.json', 'r') as db:
            db_games = json.loads(db.read())
            assert db_games['appid'] == parsed['appid']
            assert db_games['name'] == parsed['name']
            assert db_games['description'] == parsed['description']
            assert len(db_games['developers']) == len(parsed['developers'])

def test_parse_game_exception():
    except_situation = parse_game('{bla bla}, 730', 730)
    assert except_situation is None
