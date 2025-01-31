import pytest
from unittest.mock import MagicMock, patch
from controllers.audio_controller import AudioController
import numpy as np


@pytest.fixture
def config():
    return {"sample_rate": 44100, "channels": 2}


@pytest.fixture
def write_log():
    return MagicMock()


@pytest.fixture
def update_progress():
    return MagicMock()


@pytest.fixture
def audio_controller(config, write_log, update_progress):
    with patch("controllers.audio_controller.AudioDevice") as MockAudioDevice, patch(
        "controllers.audio_controller.AudioProcessor"
    ) as MockAudioProcessor, patch(
        "controllers.audio_controller.ModelManager"
    ) as MockModelManager:
        return AudioController(config, write_log, update_progress)


def test_load_models(audio_controller):
    audio_controller.load_models()
    audio_controller.model_manager.load_models.assert_called_once()


def test_start_recording(audio_controller):
    audio_callback = MagicMock()
    audio_controller.start_recording(audio_callback)
    assert audio_controller.is_recording is True
    audio_controller.audio_device.start_recording.assert_called_once_with(
        audio_callback
    )


def test_stop_recording(audio_controller):
    audio_controller.audio_data = [np.array([1, 2, 3]), np.array([4, 5, 6])]
    audio_controller.stop_recording()
    assert audio_controller.is_recording is False
    audio_controller.audio_device.stop_recording.assert_called_once()
    audio_controller.audio_processor.process_audio.assert_called_once()
    assert audio_controller.audio_data == []


def test_stop_recording_no_data(audio_controller):
    audio_controller.audio_data = []
    audio_controller.stop_recording()
    assert audio_controller.is_recording is False
    audio_controller.audio_device.stop_recording.assert_called_once()
    audio_controller.audio_processor.process_audio.assert_not_called()
