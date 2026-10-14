"""Local LLM tests use mocks; no model download needed."""
import unittest
from unittest.mock import patch
from scraper.scrape import ScrapeError, parse_with_local_model

ONE = [{"casino":"PlayaBets","raw_text":"Casino: PlayaBets | Welcome bonus: 100% up to R3,000 | Wagering requirements: 6x | Minimum deposit: R10"}]

class LocalModelTests(unittest.TestCase):
    @patch("scraper.local_model.extract_multiplier", return_value=6)
    def test_real_model_step_produces_source_grounded_field(self, mock_model):
        parsed = parse_with_local_model(ONE)
        self.assertEqual(parsed[0]["wagering_multiplier"], 6)
        self.assertEqual(parsed[0]["minimum_deposit"], "R10")
        mock_model.assert_called_once()

    @patch("scraper.local_model.extract_multiplier", return_value=600)
    def test_wrong_multiplier_is_rejected(self, _):
        with self.assertRaisesRegex(ScrapeError,"disagrees"):
            parse_with_local_model(ONE)
