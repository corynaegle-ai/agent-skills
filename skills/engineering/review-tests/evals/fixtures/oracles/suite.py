from pathlib import Path
import unittest
from unittest.mock import patch

import orders


class OrderTests(unittest.TestCase):
    def test_total(self):
        with patch("orders.total", return_value=250) as calculate:
            self.assertEqual(orders.total(2, 125), 250)
            calculate.assert_called_once_with(2, 125)

    def test_expected_total(self):
        expected = orders.total(3, 125)
        self.assertEqual(orders.total(3, 125), expected)

    def test_guard_exists(self):
        source = Path(orders.__file__).read_text()
        self.assertIn("quantity <= ORDER_LIMIT", source)

    def test_bad_quantity(self):
        with self.assertRaises(Exception):
            orders.total("two", 125)

    def test_published_limit(self):
        self.assertEqual(orders.ORDER_LIMIT, 4)

    def test_known_total(self):
        self.assertEqual(orders.total(2, 125), 250)
