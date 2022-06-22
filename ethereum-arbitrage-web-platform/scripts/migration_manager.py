import json
import os
import shutil

import yaml

from scripts.font_manager import cyan, tag


def migrate_config(path):
    print(tag("MIGRATION"), cyan("\nMigratig config...\n"))
    with open("brownie-config.yaml", "r") as brownie_config:
        config = yaml.load(brownie_config, Loader=yaml.FullLoader)

        with open(
            path + "brownieConfig.json",
            "w",
        ) as brownie_config_json:
            json.dump(config, brownie_config_json)


def migrate_builds(path):
    print(tag("MIGRATION"), cyan("\nMigratig builds...\n"))

    if os.path.exists(path + "contract_builds"):
        shutil.rmtree(path + "contract_builds")
    shutil.copytree(
        "./build",
        path + "contract_builds",
    )
