import json
import os
import shutil

import yaml


def migrate_config():
    with open("brownie-config.yaml", "r") as brownie_config:
        config = yaml.load(brownie_config, Loader=yaml.FullLoader)

        with open(
            "/Users/alex-ama/Files/GitHub/Levl-Front-End/client/src/brownieConfig.json",
            "w",
        ) as brownie_config_json:
            json.dump(config, brownie_config_json)


def migrate_builds():
    if os.path.exists(
        "/Users/alex-ama/Files/GitHub/Levl-Front-End/client/src/contract_builds"
    ):
        shutil.rmtree(
            "/Users/alex-ama/Files/GitHub/Levl-Front-End/client/src/contract_builds"
        )
    shutil.copytree(
        "./build",
        "/Users/alex-ama/Files/GitHub/Levl-Front-End/client/src/contract_builds",
    )


def main():
    migrate_config()
    migrate_builds()
