from prometheus_client import start_http_server, Gauge
import time
import requests
import HypixelMonitor.config as config


PROMETHEUS_VARS = {}


def init_prometheus(uuid):
    player_json = get_user(uuid)
    prometheus_dict = parse_player_json(player_json)

    # Init PROMETHEUS_VARS with gauges for every player
    for key, _ in prometheus_dict.items():
        # Ignore keywords
        ok = True
        for string in config.IGNORED_STRINGS:
            if string in key:
                ok = False
        if ok:
            PROMETHEUS_VARS[key] = Gauge(key, key, ["name"])


def parse_player_json(json):
    result = {}
    for gamemode in config.GAMEMODES:
        result.update(dict_to_prometheus(
            gamemode, json["player"]["stats"][gamemode]))
    return result


def dict_to_prometheus(gamemode, stats):
    result = {}
    for key, val in stats.items():
        key_txt = key.replace(' ', '_').replace('-', '_')

        if type(val) == int:
            result[gamemode + "_" + key_txt] = val
    return result


def get_user(uuid):
    params = {
        "key": config.HYPIXEL_API_KEY,
        "uuid": uuid
    }
    r = requests.get("https://api.hypixel.net/player", params=params)
    result = r.json()
    return result


if __name__ == '__main__':
    start_http_server(8000)
    print("Started logging")
    if len(config.PLAYERS) == 0:
        print("No players to search!")
        exit(0)
    init_prometheus(config.PLAYERS[0])
    while True:
        for user in config.PLAYERS:
            player_json = get_user(user)
            print("Got user data for", user)
            stats = parse_player_json(player_json)
            name = player_json["player"]["displayname"]

            for key, val in stats.items():
                if key not in PROMETHEUS_VARS:
                    continue
                PROMETHEUS_VARS[key].labels(name).set(val)

        time.sleep(config.TIMEOUT)
