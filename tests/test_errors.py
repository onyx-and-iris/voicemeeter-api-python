import pytest

import voicemeeterlib
from tests import data, vm


class TestErrors:
    __test__ = True

    def test_it_tests_an_unknown_kind(self):
        with pytest.raises(
            voicemeeterlib.error.VMError,
            match="Unknown Voicemeeter kind 'unknown_kind'",
        ):
            voicemeeterlib.api("unknown_kind")

    def test_it_tests_an_unknown_parameter(self):
        with pytest.raises(
            voicemeeterlib.error.CAPIError,
            match="VBVMR_SetParameterFloat returned -3",
        ) as exc_info:
            vm.set("unknown.parameter", 1)

        e = exc_info.value
        assert e.code == -3
        assert e.fn_name == "VBVMR_SetParameterFloat"

    def test_it_tests_an_unknown_config_name(self):
        EXPECTED_MSG = (
            "No config with name 'unknown' is loaded into memory",
            f"Known configs: {list(vm.configs.keys())}",
        )
        with pytest.raises(voicemeeterlib.error.VMError) as exc_info:
            vm.apply_config("unknown")

        e = exc_info.value
        assert e.message == "\n".join(EXPECTED_MSG)

    def test_it_tests_an_invalid_config_key(self):
        CONFIG = {
            "strip-0": {"A1": True, "B1": True, "gain": -6.0},
            "bus-0": {"mute": True, "eq": {"on": True}},
            "unknown-0": {"state": True},
            "vban-out-1": {"name": "streamname"},
        }
        with pytest.raises(ValueError, match="invalid config key 'unknown'"):
            vm.apply(CONFIG)
