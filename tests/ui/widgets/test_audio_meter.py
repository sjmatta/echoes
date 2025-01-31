import pytest
from ui.widgets.audio_meter import AudioMeter


@pytest.fixture
def audio_meter():
    return AudioMeter()


def test_compute_level_colors_low_value(audio_meter):
    result = audio_meter.compute_level_colors(0.1)
    assert result == ["green"]


def test_compute_level_colors_mid_value(audio_meter):
    result = audio_meter.compute_level_colors(0.5)
    assert result == ["green", "green", "yellow"]


def test_compute_level_colors_high_value(audio_meter):
    result = audio_meter.compute_level_colors(0.9)
    assert result == ["green", "green", "yellow", "yellow", "red"]


def test_compute_level_colors_max_value(audio_meter):
    result = audio_meter.compute_level_colors(1.0)
    assert result == ["green", "green", "yellow", "yellow", "red"]


def test_compute_level_colors_zero_value(audio_meter):
    result = audio_meter.compute_level_colors(0.0)
    assert result == ["green"]
