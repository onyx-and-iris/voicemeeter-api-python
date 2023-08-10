import os
import random
import sys
from dataclasses import dataclass

import voicemeeterlib
from voicemeeterlib.kinds import KindId
from voicemeeterlib.kinds import request_kind_map as kindmap


@dataclass
class Data:
    """bounds data to map tests to a kind"""

    name: str
    phys_in: int
    virt_in: int
    phys_out: int
    virt_out: int
    vban_in: int
    vban_out: int
    button_lower: int
    button_upper: int
    asio_in: int
    asio_out: int
    insert_lower: int
    insert_higher: int

    @property
    def channels(self):
        return (2 * self.phys_in) + (8 * self.virt_in)


# get KIND_ID from env var, otherwise set to random
KIND_ID = os.environ.get(
    "KIND", random.choice(tuple(kind_id.name.lower() for kind_id in KindId))
)
vm = voicemeeterlib.api(KIND_ID)
kind = kindmap(KIND_ID)

data = Data(
    name=kind.name,
    phys_in=kind.ins[0] - 1,
    virt_in=kind.ins[0] + kind.ins[-1] - 1,
    phys_out=kind.outs[0] - 1,
    virt_out=kind.outs[0] + kind.outs[-1] - 1,
    vban_in=kind.vban[0] - 1,
    vban_out=kind.vban[-1] - 1,
    button_lower=0,
    button_upper=79,
    asio_in=kind.asio[0] - 1,
    asio_out=kind.asio[-1] - 1,
    insert_lower=0,
    insert_higher=kind.insert - 1,
)


def setup_module():
    print(f"\nRunning tests for kind [{data.name}]\n", file=sys.stdout)
    vm.login()
    vm.command.reset()


def teardown_module():
    vm.logout()
