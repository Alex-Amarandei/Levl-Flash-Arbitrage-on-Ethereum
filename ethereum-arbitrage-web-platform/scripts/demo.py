import subprocess
import time

from scripts.deploy import deploy_all
from scripts.execute_order import execute_order
from scripts.pairs import get_pair_info


def run_price_monitor():
    p = subprocess.run(
        "python3 scripts/run_price_monitor.py",
        shell=True,
    )


def main():
    deploy_all()
    get_pair_info()
    execute_order(1)
