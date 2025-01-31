import pytest
from unittest.mock import Mock
from core.models import ModelManager


def test_model_manager_init():
    config = {
        "whisper_model": "base",
        "device": "cpu",
        "compute_type": "float32",
        "hf_token": "your_hf_token",
    }
    log_callback = Mock()
    progress_callback = Mock()

    model_manager = ModelManager(config, log_callback, progress_callback)

    assert model_manager.config == config
    assert model_manager.write_log == log_callback
    assert model_manager.update_progress == progress_callback
    assert model_manager.whisper_model is None
    assert model_manager.diarization_pipeline is None

    def test_model_manager_init():
        config = {
            "whisper_model": "base",
            "device": "cpu",
            "compute_type": "float32",
            "hf_token": "your_hf_token",
        }
        log_callback = Mock()
        progress_callback = Mock()

        model_manager = ModelManager(config, log_callback, progress_callback)

        assert model_manager.config == config
        assert model_manager.write_log == log_callback
        assert model_manager.update_progress == progress_callback
        assert model_manager.whisper_model is None
        assert model_manager.diarization_pipeline is None
