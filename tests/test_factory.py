import pytest

from tests import data, vm


class TestRemoteFactories:
    __test__ = True

    @pytest.mark.skipif(
        data.name != "basic",
        reason="Skip test if kind is not basic",
    )
    def test_it_vm_remote_attrs_for_basic(self):
        assert hasattr(vm, "strip")
        assert hasattr(vm, "bus")
        assert hasattr(vm, "command")
        assert hasattr(vm, "button")
        assert hasattr(vm, "vban")
        assert hasattr(vm, "device")
        assert hasattr(vm, "option")

        assert len(vm.strip) == 3
        assert len(vm.bus) == 2
        assert len(vm.button) == 80
        assert len(vm.vban.instream) == 4 and len(vm.vban.outstream) == 4

    @pytest.mark.skipif(
        data.name != "banana",
        reason="Skip test if kind is not banana",
    )
    def test_it_vm_remote_attrs_for_banana(self):
        assert hasattr(vm, "strip")
        assert hasattr(vm, "bus")
        assert hasattr(vm, "command")
        assert hasattr(vm, "button")
        assert hasattr(vm, "vban")
        assert hasattr(vm, "device")
        assert hasattr(vm, "option")
        assert hasattr(vm, "recorder")
        assert hasattr(vm, "patch")

        assert len(vm.strip) == 5
        assert len(vm.bus) == 5
        assert len(vm.button) == 80
        assert len(vm.vban.instream) == 8 and len(vm.vban.outstream) == 8

    @pytest.mark.skipif(
        data.name != "potato",
        reason="Skip test if kind is not potato",
    )
    def test_it_vm_remote_attrs_for_potato(self):
        assert hasattr(vm, "strip")
        assert hasattr(vm, "bus")
        assert hasattr(vm, "command")
        assert hasattr(vm, "button")
        assert hasattr(vm, "vban")
        assert hasattr(vm, "device")
        assert hasattr(vm, "option")
        assert hasattr(vm, "recorder")
        assert hasattr(vm, "patch")
        assert hasattr(vm, "fx")

        assert len(vm.strip) == 8
        assert len(vm.bus) == 8
        assert len(vm.button) == 80
        assert len(vm.vban.instream) == 8 and len(vm.vban.outstream) == 8
