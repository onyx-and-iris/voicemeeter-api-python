import pytest

from tests import data, tests


class TestRemoteFactories:
    __test__ = True

    @pytest.mark.skipif(
        data.name != "basic",
        reason="Skip test if kind is not basic",
    )
    def test_it_tests_remote_attrs_for_basic(self):
        assert hasattr(tests, "strip")
        assert hasattr(tests, "bus")
        assert hasattr(tests, "command")
        assert hasattr(tests, "button")
        assert hasattr(tests, "vban")
        assert hasattr(tests, "device")
        assert hasattr(tests, "option")

        assert len(tests.strip) == 3
        assert len(tests.bus) == 2
        assert len(tests.button) == 80
        assert len(tests.vban.instream) == 4 and len(tests.vban.outstream) == 4

    @pytest.mark.skipif(
        data.name != "banana",
        reason="Skip test if kind is not banana",
    )
    def test_it_tests_remote_attrs_for_banana(self):
        assert hasattr(tests, "strip")
        assert hasattr(tests, "bus")
        assert hasattr(tests, "command")
        assert hasattr(tests, "button")
        assert hasattr(tests, "vban")
        assert hasattr(tests, "device")
        assert hasattr(tests, "option")
        assert hasattr(tests, "recorder")
        assert hasattr(tests, "patch")

        assert len(tests.strip) == 5
        assert len(tests.bus) == 5
        assert len(tests.button) == 80
        assert len(tests.vban.instream) == 8 and len(tests.vban.outstream) == 8

    @pytest.mark.skipif(
        data.name != "potato",
        reason="Skip test if kind is not potato",
    )
    def test_it_tests_remote_attrs_for_potato(self):
        assert hasattr(tests, "strip")
        assert hasattr(tests, "bus")
        assert hasattr(tests, "command")
        assert hasattr(tests, "button")
        assert hasattr(tests, "vban")
        assert hasattr(tests, "device")
        assert hasattr(tests, "option")
        assert hasattr(tests, "recorder")
        assert hasattr(tests, "patch")
        assert hasattr(tests, "fx")

        assert len(tests.strip) == 8
        assert len(tests.bus) == 8
        assert len(tests.button) == 80
        assert len(tests.vban.instream) == 8 and len(tests.vban.outstream) == 8
