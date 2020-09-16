from prometheus_client import start_http_server, Gauge
import time
import requests
import HypixelMonitor.config as config
import HypixelMonitor.skyblock as skyblock

PROMETHEUS_VARS = {}
UUID_CACHE = {}


def get_name(uuid):
    if uuid in UUID_CACHE:
        return UUID_CACHE[uuid]
    r = requests.get(
        "https://playerdb.co/api/player/minecraft/" + uuid)
    result = r.json()
    UUID_CACHE[uuid] = result["data"]["player"]["username"]
    return UUID_CACHE[uuid]


def init_prometheus(uuid):
    """
    Create all keys that would be added to prometheus
    Needs a uuid to get his statistics
    Stores in PROMETHEUS_VARS for easy access
    """
    player_json = get_user(uuid)
    prometheus_dict = parse_player_json(player_json)

    for key in config.FORCED_STATS:
        PROMETHEUS_VARS[key] = Gauge("hypixel_" + key, key, ["name"])

    if len(config.SKYBLOCK_PROFILES) > 0:
        skyblock_dict = skyblock.prometheus(config.SKYBLOCK_PROFILES[0])
        for uuid, user in skyblock_dict["users"].items():
            for prop, _ in user.items():
                key = "hypixel_skyblock_" + prop
                PROMETHEUS_VARS[key] = Gauge(key, key, ["name", "profile"])
            break

    # Init PROMETHEUS_VARS with gauges for every player
    for key, _ in prometheus_dict.items():
        # Ignore keywords
        ok = True
        for string in config.IGNORED_STRINGS:
            if string in key:
                ok = False
        if ok:
            PROMETHEUS_VARS[key] = Gauge("hypixel_" + key, key, ["name"])


def parse_player_json(json):
    """
    Convert json from api to dict that has all keys
    that should be added to Prometheus
    """
    result = {}
    for gamemode in config.GAMEMODES:
        result.update(dict_to_prometheus(
            gamemode, json["player"]["stats"][gamemode]))
    return result


def dict_to_prometheus(gamemode, stats):
    """
    Convert json from api to dict that has all keys for a specific gamemode
    that should be added to Prometheus
    """
    result = {}
    for key, val in stats.items():
        key_txt = key.replace(' ', '_').replace('-', '_')

        if type(val) == int:
            result[gamemode + "_" + key_txt] = val
    return result


def get_user(uuid):
    """
    Retrieve json with player's statistics from hypixel api
    """
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
            UUID_CACHE[user] = name

            for key, val in stats.items():
                if key not in PROMETHEUS_VARS:
                    continue
                PROMETHEUS_VARS[key].labels(name).set(val)

            for key in config.FORCED_STATS:
                PROMETHEUS_VARS[key].labels(name).set(
                    player_json["player"][key])
        for profile in config.SKYBLOCK_PROFILES:
            skyblock_dict = skyblock.prometheus(profile)
            for uuid, user in skyblock_dict["users"].items():
                for prop, val in user.items():
                    key = "hypixel_skyblock_" + prop
                    PROMETHEUS_VARS[key].labels(
                        get_name(uuid), profile).set(val)
        time.sleep(config.TIMEOUT)
