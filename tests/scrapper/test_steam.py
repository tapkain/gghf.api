from scrapper.steam.spider import parse_game
import json


def test_parse_game():
    with open('tests/scrapper/steam_games.json', 'r') as f:
        payload = json.loads(f.read())
        game = parse_game(payload, 558620)
        assert game is not None
        game = parse_game(payload, 730)

        with open('tests/scrapper/db_games.json', 'r') as db:
            db_games = json.loads(db.read())
            assert db_games['appid'] == game['appid']
            assert db_games['name'] == game['name']
            assert db_games['description'] == game['description']
            assert len(db_games['developers']) == len(game['developers'])


def test_parse_game_exception():
    except_situation = parse_game('{bla bla}, 730', 730)
    assert except_situation is None
