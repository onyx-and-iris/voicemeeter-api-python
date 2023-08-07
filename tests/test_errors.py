import pytest

import voicemeeterlib
from tests import data, vm


class TestErrors:
    __test__ = True

    def test_it_tests_an_unknown_kind(self):
        with pytest.raises(
            voicemeeterlib.error.VMError,
            match=f"Unknown Voicemeeter kind 'unknown_kind'",
        ):
            voicemeeterlib.api("unknown_kind")

    def test_it_tests_an_unknown_parameter(self):
        with pytest.raises(
            voicemeeterlib.error.CAPIError,
            match=f"VBVMR_SetParameterFloat returned -3",
        ) as exc_info:
            vm.set("unknown.parameter", 1)

        e = exc_info.value
        assert e.code == -3
        assert e.fn_name == "VBVMR_SetParameterFloat"

    def test_it_tests_an_invalid_config(self):
        EXPECTED_MSG = (
            f"No config with name 'unknown' is loaded into memory",
            f"Known configs: {list(vm.configs.keys())}",
        )
        with pytest.raises(voicemeeterlib.error.VMError) as exc_info:
            vm.apply_config("unknown")

        e = exc_info.value
        assert e.message == "\n".join(EXPECTED_MSG)
