import pytest
from ui.widgets.processing_progress import ProcessingProgress


@pytest.fixture
def processing_progress():
    return ProcessingProgress()


def test_initial_progress(processing_progress):
    assert processing_progress.progress == 0.0
