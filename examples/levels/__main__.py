import logging
import time

import voicemeeterlib

logging.basicConfig(level=logging.INFO)


def main():
    KIND_ID = "potato"

    vm = voicemeeterlib.api(KIND_ID)
    vm.login()
    for _ in range(500):
        print(
            "\n".join(
                [
                    f"{vm.strip[5]}: {vm.strip[5].levels.postmute}",
                    f"{vm.bus[1]}: {vm.bus[0].levels.all}",
                ]
            )
        )
        time.sleep(0.033)
    vm.logout()


if __name__ == "__main__":
    main()
