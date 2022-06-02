import subprocess
import time

from scripts import deploy_contract, deploy_liquidity, deploy_tokens
from scripts.order_executor import execute_order
from scripts.pair_handler import get_pair_info


def run_price_monitor():
    p = subprocess.run(
        "python3 scripts/run_price_monitor.py",
        shell=True,
    )


def main():
    deploy_contract.main()
    deploy_tokens.main()
    deploy_liquidity.main()
    get_pair_info()
    execute_order(1)
