import unittest
from unittest.mock import Mock
from concurrent.futures import ThreadPoolExecutor
from core.processor import AudioProcessor


class TestAudioProcessorInit(unittest.TestCase):
    def setUp(self):
        self.config = {"output_dir": "/fake/dir"}
        self.model_manager = Mock()
        self.log_callback = Mock()
        self.progress_callback = Mock()

    def test_init(self):
        processor = AudioProcessor(
            config=self.config,
            model_manager=self.model_manager,
            log_callback=self.log_callback,
            progress_callback=self.progress_callback,
        )

        self.assertEqual(processor.config, self.config)
        self.assertEqual(processor.models, self.model_manager)
        self.assertEqual(processor.write_log, self.log_callback)
        self.assertEqual(processor.update_progress, self.progress_callback)
        self.assertIsInstance(processor.thread_pool, ThreadPoolExecutor)
        self.assertEqual(processor.thread_pool._max_workers, 3)


if __name__ == "__main__":
    unittest.main()
