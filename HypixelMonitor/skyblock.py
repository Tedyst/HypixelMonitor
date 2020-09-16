from prometheus_client import start_http_server, Gauge
import time
import requests
import HypixelMonitor.config as config


def prometheus(profile):
    """
    Convert json from api to dict that has all keys for a specific gamemode
    that should be added to Prometheus
    """
    profile_data = get_profile(profile)
    result = {
        "users": {}
    }
    for uuid, user in profile_data["profile"]["members"].items():
        if uuid in config.SKYBLOCK_IGNORED_PLAYERS:
            continue
        result["users"][uuid] = {
            "balance": profile_data["profile"]["banking"]["balance"],
        }
        result["users"][uuid]["skill_combat"] = user.get(
            "experience_skill_combat") or 0
        result["users"][uuid]["skill_mining"] = user.get(
            "experience_skill_mining") or 0
        result["users"][uuid]["skill_alchemy"] = user.get(
            "experience_skill_alchemy") or 0
        result["users"][uuid]["skill_farming"] = user.get(
            "experience_skill_farming") or 0
        result["users"][uuid]["skill_enchanting"] = user.get(
            "experience_skill_enchanting") or 0
        result["users"][uuid]["skill_fishing"] = user.get(
            "experience_skill_fishing") or 0
        result["users"][uuid]["skill_foraging"] = user.get(
            "experience_skill_foraging") or 0
    return result


def get_profile(profile):
    """
    Retrieve json with player's statistics from hypixel api
    """
    params = {
        "key": config.HYPIXEL_API_KEY,
        "profile": profile
    }
    r = requests.get("https://api.hypixel.net/skyblock/profile", params=params)
    result = r.json()
    return result


if __name__ == '__main__':
    for profile in config.SKYBLOCK_PROFILES:
        json_data = get_profile(profile)
