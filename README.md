# Hypixel Monitor

Exports the statistics from hypixel api and exports them to Prometheus

## Usage

```python
python main.py
```

## Config

The config is avaliable on `HypixelMonitor/config.py`.

```text
IGNORED_STRINGS = keys from api that will be ignored and not added to Prometheus
GAMEMODES = which stats to import
PLAYERS = list separated by commas that contains the uuids of people to search
HYPIXEL_API_KEY = the api key from hypixel, can be imported using env variables
FORCED_STATS = keys to import without being from stats of gamemodes
```
