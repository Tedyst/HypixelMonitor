import os

if os.getenv("HYPIXEL_API_KEY"):
    HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
else:
    print("No hypixel api key!")
    exit(0)

TIMEOUT = int(os.getenv("TIMEOUT") or 60)
PLAYERS = (os.getenv("PLAYERS")
           or "1c57e151112f4da4a229ade98a4f0c0b").split(',')
