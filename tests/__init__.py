import random
import sys
from dataclasses import dataclass

import voicemeeterlib
from voicemeeterlib.kinds import KindId
from voicemeeterlib.kinds import request_kind_map as kindmap

# let's keep things random
KIND_ID = random.choice(tuple(kind_id.name.lower() for kind_id in KindId))
vm = voicemeeterlib.api(KIND_ID)
kind = kindmap(KIND_ID)


@dataclass
class Data:
    """bounds data to map tests to a kind"""

    name: str = kind.name
    phys_in: int = kind.ins[0] - 1
    virt_in: int = kind.ins[0] + kind.ins[-1] - 1
    phys_out: int = kind.outs[0] - 1
    virt_out: int = kind.outs[0] + kind.outs[-1] - 1
    vban_in: int = kind.vban[0] - 1
    vban_out: int = kind.vban[-1] - 1
    button_lower: int = 0
    button_upper: int = 79
    asio_in: int = kind.asio[0] - 1
    asio_out: int = kind.asio[-1] - 1
    insert_lower: int = 0
    insert_higher: int = kind.insert - 1

    @property
    def channels(self):
        return (2 * self.phys_in) + (8 * self.virt_in)


data = Data()


def setup_module():
    print(f"\nRunning tests for kind [{data.name}]\n", file=sys.stdout)
    vm.login()
    vm.command.reset()


def teardown_module():
    vm.logout()
