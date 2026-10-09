import threading
import time
import unittest
from unittest.mock import Mock

from worker import run_job


class WorkerTests(unittest.TestCase):
    def test_background_job_completes(self):
        entered, release = threading.Event(), threading.Event()
        thread = threading.Thread(target=run_job, args=(lambda: 3, entered, release))
        thread.start()
        time.sleep(0.01)
        self.assertTrue(thread.is_alive())
        release.set()
        thread.join(1)
        self.assertFalse(thread.is_alive())

    def test_deadline_prevents_callback(self):
        callback = Mock()
        with self.assertRaises(TimeoutError):
            run_job(callback, threading.Event(), threading.Event(), wait_seconds=0.01)
        callback.assert_not_called()
