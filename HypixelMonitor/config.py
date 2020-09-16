import os

if os.getenv("HYPIXEL_API_KEY"):
    HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
else:
    print("No hypixel api key!")
    exit(0)

TIMEOUT = int(os.getenv("TIMEOUT") or 60)
PLAYERS = (os.getenv("PLAYERS")
           or "1c57e151112f4da4a229ade98a4f0c0b").split(',')
GAMEMODES = [
    "SkyWars",
    "Bedwars"
]
FORCED_STATS = [
    "karma",
    "networkExp"
]
IGNORED_STRINGS = [
    # SkyWars
    "castle",
    "longest_bow_kill",
    "lab",
    "votes",
    "chests",
    "mega",
    "fastest",
    "quickjoin",
    "kit",
    "inGamePresentsCap",
    "heads",
    "lastHytaleAd",
    "lastTourneyAd",
    "items_purchased",
    "instant_smelting",
    "nourishment",
    "xezbeth",
    "soul_well",
    "knowledge",
    "resistance_boost",
    "mining_expertise",
    "ender_mastery",
    "lucky_charm",
    "juggernaut",
    "arrow_recovery",
    "black_magic",
    "necromancer",
    "explained",
    "challenge",
    # BedWars
    "box",
    "openedEpics",
    "ultimate"
]

SKYBLOCK_PROFILES = (os.getenv("SKYBLOCK_PROFILES")
                     or "737984c653a944df8a71c049618c92b6").split(',')
