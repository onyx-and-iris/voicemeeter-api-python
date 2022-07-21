import time

import pytest

from tests import data, tests


class TestUserConfigs:
    __test__ = True

    """example config tests"""

    @classmethod
    def setup_class(cls):
        tests.apply_config("example")

    def test_it_tests_config_string(self):
        assert "PhysStrip" in tests.strip[data.phys_in].label
        assert "VirtStrip" in tests.strip[data.virt_in].label
        assert "PhysBus" in tests.bus[data.phys_out].label
        assert "VirtBus" in tests.bus[data.virt_out].label

    def test_it_tests_config_bool(self):
        assert tests.strip[0].A1 == True

    @pytest.mark.skipif(
        "not config.getoption('--run-slow')",
        reason="Only run when --run-slow is given",
    )
    def test_it_tests_config_busmode(self):
        assert tests.bus[data.phys_out].mode.get() == "composite"

    def test_it_tests_config_bass_med_high(self):
        assert tests.strip[data.virt_in].bass == -3.2
        assert tests.strip[data.virt_in].mid == 1.5
        assert tests.strip[data.virt_in].high == 2.1
