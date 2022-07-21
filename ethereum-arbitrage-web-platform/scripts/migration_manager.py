import json
import os
import shutil

import yaml

from scripts.font_manager import cyan, green, tag


def migrate_config(path):
    print(tag("MIGRATION"), cyan("Migrating config..."))
    with open("brownie-config.yaml", "r") as brownie_config:
        config = yaml.load(brownie_config, Loader=yaml.FullLoader)

        with open(
            path + "brownieConfig.json",
            "w",
        ) as brownie_config_json:
            json.dump(config, brownie_config_json)
    print(tag("MIGRATION"), green("Done!"))


def migrate_builds(path):
    print(tag("MIGRATION"), cyan("Migrating builds..."))

    if os.path.exists(path + "contract_builds"):
        shutil.rmtree(path + "contract_builds")
    shutil.copytree(
        "./build",
        path + "contract_builds",
    )
    print(tag("MIGRATION"), green("Done!"))


def main():
    # Complete with the path to the src folder in the front end
    path = "client/src/"

    migrate_config(path)
    migrate_builds(path)
