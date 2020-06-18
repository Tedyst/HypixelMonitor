from prometheus_client import start_http_server, Gauge
import time
import requests
import HypixelMonitor.config as config

HYPIXEL_EXP = Gauge('hypixel_exp', 'Network EXP', ["name"])
SKYWARS_SOULS = Gauge('hypixel_skywars_souls', 'SkyWars Souls', ["name"])
SKYWARS_WIN_STREAK = Gauge('hypixel_skywars_win_streak',
                           'SkyWars Win Streak', ["name"])
BEDWARS_EXP = Gauge('hypixel_bedwars_exp', 'BedWars EXP', ["name"])
BEDWARS_WIN_STREAK = Gauge('hypixel_bedwars_win_streak',
                           'BedWars Win Streak', ["name"])
BEDWARS_COINS = Gauge('hypixel_bedwars_coins', 'BedWars Coins', ["name"])
KARMA = Gauge('hypixel_karma', 'Karma', ["name"])


def getUser(uuid):
    params = {
        "key": config.HYPIXEL_API_KEY,
        "uuid": uuid
    }
    r = requests.get("https://api.hypixel.net/player", params=params)
    result = r.json()
    name = result["player"]["displayname"]

    xp = result["player"]["networkExp"]
    HYPIXEL_EXP.labels(name).set(xp)

    skywars_souls = result["player"]["stats"]["SkyWars"]["souls"]
    SKYWARS_SOULS.labels(name).set(skywars_souls)
    skywars_win_streak = result["player"]["stats"]["SkyWars"]["win_streak"]
    SKYWARS_WIN_STREAK.labels(name).set(skywars_win_streak)
    bedwars_exp = result["player"]["stats"]["Bedwars"]["Experience"]
    BEDWARS_EXP.labels(name).set(bedwars_exp)
    bedwars_win_streak = result["player"]["stats"]["Bedwars"]["winstreak"]
    BEDWARS_WIN_STREAK.labels(name).set(bedwars_win_streak)
    bedwars_coins = result["player"]["stats"]["Bedwars"]["coins"]
    BEDWARS_COINS.labels(name).set(bedwars_coins)
    karma = result["player"]["karma"]
    KARMA.labels(name).set(karma)


if __name__ == '__main__':
    start_http_server(8000)
    print("Started logging")
    while True:
        for user in config.PLAYERS:
            getUser(user)
            print("Got user data for", user)
        time.sleep(config.TIMEOUT)
