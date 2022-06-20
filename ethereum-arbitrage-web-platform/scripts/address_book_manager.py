import json

from brownie import config


def get_address_at(name, source="map"):
    if source == "map":
        with open("build/deployments/map.json", "r") as map_json_file:
            map_json = json.load(map_json_file)

            return map_json["4"][name][0]
    else:
        if len(name) == 1:
            return config["networks"]["rinkeby"][name[0]]
        elif len(name) == 2:
            return config["networks"]["rinkeby"][name[0]][name[1]]
