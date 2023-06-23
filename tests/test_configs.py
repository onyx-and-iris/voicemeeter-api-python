import pytest

from tests import data, vm


class TestUserConfigs:
    __test__ = True

    """example config vm"""

    @classmethod
    def setup_class(cls):
        vm.apply_config("example")

    def test_it_vm_config_string(self):
        assert "PhysStrip" in vm.strip[data.phys_in].label
        assert "VirtStrip" in vm.strip[data.virt_in].label
        assert "PhysBus" in vm.bus[data.phys_out].label
        assert "VirtBus" in vm.bus[data.virt_out].label

    def test_it_vm_config_bool(self):
        assert vm.strip[0].A1 == True

    @pytest.mark.skipif(
        data.name != "potato",
        reason="Skip test if kind is not potato",
    )
    def test_it_vm_config_bool_strip_eq_on(self):
        assert vm.strip[data.phys_in].eq.on == True

    @pytest.mark.skipif(
        data.name != "banana",
        reason="Skip test if kind is not banana",
    )
    def test_it_vm_config_bool_bus_eq_ab(self):
        assert vm.bus[data.phys_out].eq.ab == True

    @pytest.mark.skipif(
        "not config.getoption('--run-slow')",
        reason="Only run when --run-slow is given",
    )
    def test_it_vm_config_busmode(self):
        assert vm.bus[data.phys_out].mode.get() == "composite"

    def test_it_vm_config_bass_med_high(self):
        assert vm.strip[data.virt_in].bass == -3.2
        assert vm.strip[data.virt_in].mid == 1.5
        assert vm.strip[data.virt_in].high == 2.1
