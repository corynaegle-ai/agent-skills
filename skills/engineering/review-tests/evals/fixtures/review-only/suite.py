from pathlib import Path
import unittest
from unittest.mock import Mock

import sender


class SenderTests(unittest.TestCase):
    def test_repeated_key_sends_once(self):
        transport = Mock()
        transport.send.return_value = "receipt-17"
        service = sender.Sender(transport)
        first = service.send("key-1", "hello")
        second = service.send("key-1", "hello")
        self.assertEqual((first, second), ("receipt-17", "receipt-17"))
        transport.send.assert_called_once_with({"version": 1, "key": "key-1", "text": "hello"})

    def test_required_source(self):
        self.assertIn("self.receipts[key] = receipt", Path(sender.__file__).read_text())

    @unittest.skip("requires unavailable live delivery service")
    def test_live_delivery(self):
        self.fail("live service is unavailable in this fixture")
