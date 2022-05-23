import subprocess
import time

if __name__ == "__main__":
    while True:
        p = subprocess.run(
            "brownie run scripts/get_pair_price.py --network mainnet",
            shell=True,
        )
        time.sleep(20)
