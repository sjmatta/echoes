import pytest
import sounddevice as sd
from unittest.mock import MagicMock, patch
from core.audio import AudioDevice


@pytest.fixture
def audio_device():
    return AudioDevice()


def test_start_recording(audio_device):
    callback = MagicMock()
    with patch.object(sd, "InputStream", return_value=MagicMock()) as mock_stream:
        audio_device.start_recording(callback)
        mock_stream.assert_called_once_with(
            callback=callback, channels=1, samplerate=16000
        )
        mock_stream.return_value.start.assert_called_once()


def test_start_recording_exception(audio_device):
    callback = MagicMock()
    with patch.object(sd, "InputStream", side_effect=Exception("Test Error")):
        with pytest.raises(RuntimeError, match="Error starting recording: Test Error"):
            audio_device.start_recording(callback)


def test_stop_recording(audio_device):
    mock_stream = MagicMock()
    audio_device._stream = mock_stream
    audio_device.stop_recording()
    mock_stream.stop.assert_called_once()
    mock_stream.close.assert_called_once()
    assert audio_device._stream is None


def test_stop_recording_no_stream(audio_device):
    audio_device.stop_recording()
    assert audio_device._stream is None
