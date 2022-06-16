import pytest

from tests import data, tests


class TestSetAndGetFloatLower:
    __test__ = True

    """VBVMR_SetParameterFloat, VBVMR_GetParameterFloat"""

    @pytest.mark.parametrize(
        "param,value",
        [
            (f"Strip[{data.phys_in}].Mute", 1),
            (f"Bus[{data.virt_out}].Eq.on", 1),
            (f"Strip[{data.phys_in}].Mute", 0),
            (f"Bus[{data.virt_out}].Eq.on", 0),
        ],
    )
    def test_it_sets_and_gets_mute_eq_float_params(self, param, value):
        tests.set(param, value)
        assert (round(tests.get(param))) == value

    @pytest.mark.parametrize(
        "param,value",
        [
            (f"Strip[{data.phys_in}].Comp", 5.3),
            (f"Strip[{data.virt_in}].Gain", -37.5),
            (f"Bus[{data.virt_out}].Gain", -22.7),
        ],
    )
    def test_it_sets_and_gets_comp_gain_float_params(self, param, value):
        tests.set(param, value)
        assert (round(tests.get(param), 1)) == value


@pytest.mark.parametrize("value", ["test0", "test1"])
class TestSetAndGetStringLower:
    __test__ = True

    """VBVMR_SetParameterStringW, VBVMR_GetParameterStringW"""

    @pytest.mark.parametrize(
        "param",
        [(f"Strip[{data.phys_out}].label"), (f"Bus[{data.virt_out}].label")],
    )
    def test_it_sets_and_gets_string_params(self, param, value):
        tests.set(param, value)
        assert tests.get(param, string=True) == value


@pytest.mark.parametrize("value", [0, 1])
class TestMacroButtonsLower:
    """VBVMR_MacroButton_SetStatus, VBVMR_MacroButton_GetStatus"""

    @pytest.mark.parametrize(
        "index, mode",
        [(33, 1), (49, 1)],
    )
    def test_it_sets_and_gets_macrobuttons_state(self, index, mode, value):
        tests.set_buttonstatus(index, value, mode)
        assert tests.get_buttonstatus(index, mode) == value

    @pytest.mark.parametrize(
        "index, mode",
        [(14, 2), (12, 2)],
    )
    def test_it_sets_and_gets_macrobuttons_stateonly(self, index, mode, value):
        tests.set_buttonstatus(index, value, mode)
        assert tests.get_buttonstatus(index, mode) == value

    @pytest.mark.parametrize(
        "index, mode",
        [(50, 3), (65, 3)],
    )
    def test_it_sets_and_gets_macrobuttons_trigger(self, index, mode, value):
        tests.set_buttonstatus(index, value, mode)
        assert tests.get_buttonstatus(index, mode) == value
