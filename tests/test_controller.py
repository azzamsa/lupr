import pytest

import Lupr.controllers.controller
from Lupr.controllers.controller import Controller
from Lupr.model.model import Model
from tests.fakes.controller_fake import FakePopen


class TestController:
    @pytest.fixture
    def ctrl(self):
        """Controller fixture"""
        model = Model()
        ctrl = Controller(model)
        return ctrl

    def test_get_all_windows_with_monkeypatch(self, ctrl, monkeypatch):
        """Test get_all_windows with monkeypatch to Popen."""

        window_title = b"0x006000ab  0 machine-name foo_window_title"

        def fake_communicate(input=None, timeout=None):
            return window_title, "err"

        monkeypatch.setattr(Lupr.controllers.controller, "Popen", FakePopen)
        monkeypatch.setattr(
            Lupr.controllers.controller.Popen, "communicate", fake_communicate
        )
        output = ctrl.get_all_windows()
        assert output == "foo_window_title\n"

    def test_get_all_windows_with_fake(self, ctrl, monkeypatch):
        """Test get_all_windows with Fake Object."""
        window_title = b"0x006000ab  0 machine-name foo_window_title"

        def fake_communicate(input=None, timeout=None):
            return window_title, "err"

        Lupr.controllers.controller.Popen = FakePopen
        Lupr.controllers.controller.Popen.communicate = fake_communicate

        output = ctrl.get_all_windows()
        assert output == "foo_window_title\n"

    def test_get_all_windows_no_windows(self, ctrl, monkeypatch):
        """Test get_all_windows with Fake Object."""
        window_title = None

        def fake_communicate(input=None, timeout=None):
            return window_title, "err"

        Lupr.controllers.controller.Popen = FakePopen
        Lupr.controllers.controller.Popen.communicate = fake_communicate

        output = ctrl.get_all_windows()
        assert output == ""
