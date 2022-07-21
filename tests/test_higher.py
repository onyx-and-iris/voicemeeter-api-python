import pytest

from tests import data, tests


@pytest.mark.parametrize("value", [False, True])
class TestSetAndGetBoolHigher:
    __test__ = True

    """strip tests, physical and virtual"""

    @pytest.mark.parametrize(
        "index,param",
        [
            (data.phys_in, "mute"),
            (data.phys_in, "mono"),
            (data.virt_in, "mc"),
            (data.virt_in, "mono"),
        ],
    )
    def test_it_sets_and_gets_strip_bool_params(self, index, param, value):
        setattr(tests.strip[index], param, value)
        assert getattr(tests.strip[index], param) == value

    """ bus tests, physical and virtual """

    @pytest.mark.parametrize(
        "index,param",
        [
            (data.phys_out, "eq"),
            (data.phys_out, "mute"),
            (data.virt_out, "eq_ab"),
            (data.virt_out, "sel"),
        ],
    )
    def test_it_sets_and_gets_bus_bool_params(self, index, param, value):
        setattr(tests.bus[index], param, value)
        assert getattr(tests.bus[index], param) == value

    """  bus modes tests, physical and virtual """

    @pytest.mark.skipif(
        data.name != "basic",
        reason="Skip test if kind is not basic",
    )
    @pytest.mark.parametrize(
        "index,param",
        [
            (data.phys_out, "normal"),
            (data.phys_out, "amix"),
            (data.virt_out, "normal"),
            (data.virt_out, "composite"),
        ],
    )
    def test_it_sets_and_gets_busmode_basic_bool_params(self, index, param, value):
        setattr(tests.bus[index].mode, param, value)
        assert getattr(tests.bus[index].mode, param) == value

    @pytest.mark.skipif(
        data.name == "basic",
        reason="Skip test if kind is basic",
    )
    @pytest.mark.parametrize(
        "index,param",
        [
            (data.phys_out, "normal"),
            (data.phys_out, "amix"),
            (data.phys_out, "rearonly"),
            (data.virt_out, "normal"),
            (data.virt_out, "upmix41"),
            (data.virt_out, "composite"),
        ],
    )
    def test_it_sets_and_gets_busmode_bool_params(self, index, param, value):
        setattr(tests.bus[index].mode, param, value)
        assert getattr(tests.bus[index].mode, param) == value

    """ macrobutton tests """

    @pytest.mark.parametrize(
        "index,param",
        [(data.button_lower, "state"), (data.button_upper, "trigger")],
    )
    def test_it_sets_and_gets_macrobutton_bool_params(self, index, param, value):
        setattr(tests.button[index], param, value)
        assert getattr(tests.button[index], param) == value

    """ vban instream tests """

    @pytest.mark.parametrize(
        "index,param",
        [(data.vban_in, "on")],
    )
    def test_it_sets_and_gets_vban_instream_bool_params(self, index, param, value):
        setattr(tests.vban.instream[index], param, value)
        assert getattr(tests.vban.instream[index], param) == value

    """ vban outstream tests """

    @pytest.mark.parametrize(
        "index,param",
        [(data.vban_out, "on")],
    )
    def test_it_sets_and_gets_vban_outstream_bool_params(self, index, param, value):
        setattr(tests.vban.outstream[index], param, value)
        assert getattr(tests.vban.outstream[index], param) == value

    """ command tests """

    @pytest.mark.parametrize(
        "param",
        [("lock")],
    )
    def test_it_sets_command_bool_params(self, param, value):
        setattr(tests.command, param, value)

    """ recorder tests """

    @pytest.mark.skipif(
        data.name == "basic",
        reason="Skip test if kind is basic",
    )
    @pytest.mark.parametrize(
        "param",
        [("A1"), ("B2")],
    )
    def test_it_sets_and_gets_recorder_bool_params(self, param, value):
        setattr(tests.recorder, param, value)
        assert getattr(tests.recorder, param) == value

    @pytest.mark.skipif(
        data.name == "basic",
        reason="Skip test if kind is basic",
    )
    @pytest.mark.parametrize(
        "param",
        [("loop")],
    )
    def test_it_sets_recorder_bool_params(self, param, value):
        setattr(tests.recorder, param, value)

    """ fx tests """

    @pytest.mark.skipif(
        data.name != "potato",
        reason="Skip test if kind is not potato",
    )
    @pytest.mark.parametrize(
        "param",
        [("reverb"), ("reverb_ab"), ("delay"), ("delay_ab")],
    )
    def test_it_sets_and_gets_fx_bool_params(self, param, value):
        setattr(tests.fx, param, value)
        assert getattr(tests.fx, param) == value

    """ patch tests """

    @pytest.mark.skipif(
        data.name == "basic",
        reason="Skip test if kind is basic",
    )
    @pytest.mark.parametrize(
        "param",
        [("postfadercomposite")],
    )
    def test_it_sets_and_gets_patch_bool_params(self, param, value):
        setattr(tests.patch, param, value)
        assert getattr(tests.patch, param) == value

    """ patch.insert tests """

    @pytest.mark.skipif(
        data.name == "basic",
        reason="Skip test if kind is basic",
    )
    @pytest.mark.parametrize(
        "index, param",
        [(data.insert_lower, "on"), (data.insert_higher, "on")],
    )
    def test_it_sets_and_gets_patch_insert_bool_params(self, index, param, value):
        setattr(tests.patch.insert[index], param, value)
        assert getattr(tests.patch.insert[index], param) == value

    """ option tests """

    @pytest.mark.parametrize(
        "param",
        [("monitoronsel")],
    )
    def test_it_sets_and_gets_option_bool_params(self, param, value):
        setattr(tests.option, param, value)
        assert getattr(tests.option, param) == value


class TestSetAndGetIntHigher:
    __test__ = True

    """strip tests, physical and virtual"""

    @pytest.mark.parametrize(
        "index,param,value",
        [
            (data.phys_in, "limit", -40),
            (data.phys_in, "limit", 12),
            (data.virt_in, "k", 0),
            (data.virt_in, "k", 4),
        ],
    )
    def test_it_sets_and_gets_strip_bool_params(self, index, param, value):
        setattr(tests.strip[index], param, value)
        assert getattr(tests.strip[index], param) == value

    """ vban outstream tests """

    @pytest.mark.parametrize(
        "index,param,value",
        [(data.vban_out, "sr", 48000)],
    )
    def test_it_sets_and_gets_vban_outstream_bool_params(self, index, param, value):
        setattr(tests.vban.outstream[index], param, value)
        assert getattr(tests.vban.outstream[index], param) == value

    """ patch.asio tests """

    @pytest.mark.skipif(
        data.name == "basic",
        reason="Skip test if kind is basic",
    )
    @pytest.mark.parametrize(
        "index,value",
        [
            (0, 1),
            (data.asio_in, 4),
        ],
    )
    def test_it_sets_and_gets_patch_asio_in_int_params(self, index, value):
        tests.patch.asio[index].set(value)
        assert tests.patch.asio[index].get() == value

    """ patch.A2[i]-A5[i] tests """

    @pytest.mark.skipif(
        data.name == "basic",
        reason="Skip test if kind is basic",
    )
    @pytest.mark.parametrize(
        "index,value",
        [
            (0, 1),
            (data.asio_out, 4),
        ],
    )
    def test_it_sets_and_gets_patch_asio_out_int_params(self, index, value):
        tests.patch.A2[index].set(value)
        assert tests.patch.A2[index].get() == value
        tests.patch.A5[index].set(value)
        assert tests.patch.A5[index].get() == value

    """ patch.composite tests """

    @pytest.mark.skipif(
        data.name == "basic",
        reason="Skip test if kind is basic",
    )
    @pytest.mark.parametrize(
        "index,value",
        [
            (0, 3),
            (0, data.channels),
            (7, 8),
            (7, data.channels),
        ],
    )
    def test_it_sets_and_gets_patch_composite_int_params(self, index, value):
        tests.patch.composite[index].set(value)
        assert tests.patch.composite[index].get() == value

    """ option tests """

    @pytest.mark.skipif(
        data.name == "basic",
        reason="Skip test if kind is basic",
    )
    @pytest.mark.parametrize(
        "index,value",
        [
            (data.phys_out, 30),
            (data.phys_out, 500),
        ],
    )
    def test_it_sets_and_gets_patch_delay_int_params(self, index, value):
        tests.option.delay[index].set(value)
        assert tests.option.delay[index].get() == value


class TestSetAndGetFloatHigher:
    __test__ = True

    """strip tests, physical and virtual"""

    @pytest.mark.parametrize(
        "index,param,value",
        [
            (data.phys_in, "gain", -3.6),
            (data.virt_in, "gain", 5.8),
            (data.phys_in, "comp", 0.0),
            (data.virt_in, "comp", 8.2),
            (data.phys_in, "gate", 2.3),
            (data.virt_in, "gate", 6.7),
        ],
    )
    def test_it_sets_and_gets_strip_float_params(self, index, param, value):
        setattr(tests.strip[index], param, value)
        assert getattr(tests.strip[index], param) == value

    @pytest.mark.parametrize(
        "index,value",
        [(data.phys_in, 2), (data.phys_in, 2), (data.virt_in, 8), (data.virt_in, 8)],
    )
    def test_it_gets_prefader_levels_and_compares_length_of_array(self, index, value):
        assert len(tests.strip[index].levels.prefader) == value

    @pytest.mark.parametrize(
        "index,value",
        [(data.phys_in, 2), (data.phys_in, 2), (data.virt_in, 8), (data.virt_in, 8)],
    )
    def test_it_gets_postmute_levels_and_compares_length_of_array(self, index, value):
        assert len(tests.strip[index].levels.postmute) == value

    @pytest.mark.skipif(
        data.name != "potato",
        reason="Only test if logged into Potato version",
    )
    @pytest.mark.parametrize(
        "index, j, value",
        [
            (data.phys_in, 0, -20.7),
            (data.virt_in, 3, -60),
            (data.virt_in, 4, 3.6),
            (data.phys_in, 4, -12.7),
        ],
    )
    def test_it_sets_and_gets_strip_gainlayer_values(self, index, j, value):
        tests.strip[index].gainlayer[j].gain = value
        assert tests.strip[index].gainlayer[j].gain == value

    """ strip tests, physical """

    @pytest.mark.parametrize(
        "index, param, value",
        [
            (data.phys_in, "pan_x", -0.6),
            (data.phys_in, "pan_x", 0.6),
            (data.phys_in, "color_y", 0.8),
            (data.phys_in, "fx_x", -0.6),
        ],
    )
    def test_it_sets_and_gets_strip_xy_params(self, index, param, value):
        assert hasattr(tests.strip[index], param)
        setattr(tests.strip[index], param, value)
        assert getattr(tests.strip[index], param) == value

    @pytest.mark.skipif(
        data.name != "potato",
        reason="Only test if logged into Potato version",
    )
    @pytest.mark.parametrize(
        "index, param, value",
        [
            (data.phys_in, "reverb", -1.6),
            (data.phys_in, "postfx1", True),
        ],
    )
    def test_it_sets_and_gets_strip_effects_params(self, index, param, value):
        assert hasattr(tests.strip[index], param)
        setattr(tests.strip[index], param, value)
        assert getattr(tests.strip[index], param) == value

    """ strip tests, virtual """

    @pytest.mark.parametrize(
        "index, param, value",
        [
            (data.virt_in, "treble", -1.6),
            (data.virt_in, "mid", 5.8),
            (data.virt_in, "bass", -8.1),
        ],
    )
    def test_it_sets_and_gets_strip_eq_params(self, index, param, value):
        setattr(tests.strip[index], param, value)
        assert getattr(tests.strip[index], param) == value

    """ bus tests, physical and virtual """

    @pytest.mark.skipif(
        data.name != "potato",
        reason="Only test if logged into Potato version",
    )
    @pytest.mark.parametrize(
        "index, param, value",
        [(data.phys_out, "returnreverb", 3.6), (data.virt_out, "returnfx1", 5.8)],
    )
    def test_it_sets_and_gets_bus_effects_float_params(self, index, param, value):
        assert hasattr(tests.bus[index], param)
        setattr(tests.bus[index], param, value)
        assert getattr(tests.bus[index], param) == value

    @pytest.mark.parametrize(
        "index, param, value",
        [(data.phys_out, "gain", -3.6), (data.virt_out, "gain", 5.8)],
    )
    def test_it_sets_and_gets_bus_float_params(self, index, param, value):
        setattr(tests.bus[index], param, value)
        assert getattr(tests.bus[index], param) == value

    @pytest.mark.parametrize(
        "index,value",
        [(data.phys_out, 8), (data.virt_out, 8)],
    )
    def test_it_gets_prefader_levels_and_compares_length_of_array(self, index, value):
        assert len(tests.bus[index].levels.all) == value


@pytest.mark.parametrize("value", ["test0", "test1"])
class TestSetAndGetStringHigher:
    __test__ = True

    """strip tests, physical and virtual"""

    @pytest.mark.parametrize(
        "index, param",
        [(data.phys_in, "label"), (data.virt_in, "label")],
    )
    def test_it_sets_and_gets_strip_string_params(self, index, param, value):
        setattr(tests.strip[index], param, value)
        assert getattr(tests.strip[index], param) == value

    """ bus tests, physical and virtual """

    @pytest.mark.parametrize(
        "index, param",
        [(data.phys_out, "label"), (data.virt_out, "label")],
    )
    def test_it_sets_and_gets_bus_string_params(self, index, param, value):
        setattr(tests.bus[index], param, value)
        assert getattr(tests.bus[index], param) == value

    """ vban instream tests """

    @pytest.mark.parametrize(
        "index, param",
        [(data.vban_in, "name")],
    )
    def test_it_sets_and_gets_vban_instream_string_params(self, index, param, value):
        setattr(tests.vban.instream[index], param, value)
        assert getattr(tests.vban.instream[index], param) == value

    """ vban outstream tests """

    @pytest.mark.parametrize(
        "index, param",
        [(data.vban_out, "name")],
    )
    def test_it_sets_and_gets_vban_outstream_string_params(self, index, param, value):
        setattr(tests.vban.outstream[index], param, value)
        assert getattr(tests.vban.outstream[index], param) == value


@pytest.mark.parametrize("value", [False, True])
class TestSetAndGetMacroButtonHigher:
    __test__ = True

    """macrobutton tests"""

    @pytest.mark.parametrize(
        "index, param",
        [
            (0, "state"),
            (39, "stateonly"),
            (69, "trigger"),
            (22, "stateonly"),
            (45, "state"),
            (65, "trigger"),
        ],
    )
    def test_it_sets_and_gets_macrobutton_params(self, index, param, value):
        setattr(tests.button[index], param, value)
        assert getattr(tests.button[index], param) == value
