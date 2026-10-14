"""Offline tests: do not contact the public source or AI API."""
import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from scraper.scrape import ScrapeError, collect_bonus_cards, fetch_page, parse_with_llm

HTML = (Path(__file__).parent / "fixtures/listing.html").read_text(encoding="utf-8")

class ScraperTests(unittest.TestCase):
    def test_three_complete_casinos(self):
        cards = collect_bonus_cards(HTML)
        self.assertEqual([c["casino"] for c in cards], ["PlayaBets","Springbok Casino","Thunderbolt Casino"])
        self.assertIn("Minimum deposit: R10", cards[0]["raw_text"])

    def test_missing_table_fails(self):
        with self.assertRaises(ScrapeError):
            collect_bonus_cards("<html><body>Unavailable</body></html>")

    def test_ambiguous_wager_fails(self):
        with self.assertRaisesRegex(ScrapeError, "ambiguous"):
            collect_bonus_cards(HTML.replace("<td>6x</td>", "<td>6x sports / 30x casino</td>"))

    def test_robots_disallow_fails_closed(self):
        session = Mock()
        session.get.return_value = Mock(status_code=200, text="User-agent: *\nDisallow: /casino-bonuses-south-africa/")
        with self.assertRaisesRegex(ScrapeError,"disallows"):
            fetch_page(session)
        self.assertEqual(session.get.call_count,1)

    def test_robots_redirect_fails_closed(self):
        session = Mock()
        session.get.return_value = Mock(status_code=301)
        with self.assertRaisesRegex(ScrapeError,"robots.txt HTTP 301"):
            fetch_page(session)

    def test_page_block_fails(self):
        session = Mock()
        session.get.side_effect = [Mock(status_code=404), Mock(status_code=403)]
        with self.assertRaisesRegex(ScrapeError,"403"):
            fetch_page(session)

    @patch("scraper.scrape.api_settings",return_value=("https://example.invalid/llm","fake","fake"))
    def test_llm_validates_and_rejects_invented_numbers(self,_):
        cards = collect_bonus_cards(HTML)
        rows = [
            {"casino":"PlayaBets","welcome_bonus":"100% up to R3,000","wagering_raw":"6x","wagering_multiplier":6,"wagering_basis":"unspecified","minimum_deposit":"R10"},
            {"casino":"Springbok Casino","welcome_bonus":"R250 no-deposit + up to R11,500 (3 deposits)","wagering_raw":"30x","wagering_multiplier":30,"wagering_basis":"unspecified","minimum_deposit":"R25"},
            {"casino":"Thunderbolt Casino","welcome_bonus":"Up to R10,000 (4 coupons)","wagering_raw":"30x","wagering_multiplier":30,"wagering_basis":"unspecified","minimum_deposit":"R25"}
        ]
        session=Mock()
        session.post.return_value.json.return_value={"choices":[{"message":{"content":"\u0060\u0060\u0060json\n"+json.dumps({"records":rows})+"\n\u0060\u0060\u0060"}}]}
        validated=parse_with_llm(session,cards)
        self.assertEqual([r["wagering_multiplier"] for r in validated],[6,30,30])
        self.assertEqual(validated[0]["wagering_basis"],"unspecified")
        rows[0]["wagering_multiplier"]=600
        session.post.return_value.json.return_value={"choices":[{"message":{"content":json.dumps({"records":rows})}}]}
        with self.assertRaisesRegex(ScrapeError,"differs from source"):
            parse_with_llm(session,cards)
        rows[0]["wagering_multiplier"]=6
        rows[0]["minimum_deposit"]="R1000"
        session.post.return_value.json.return_value={"choices":[{"message":{"content":json.dumps({"records":rows})}}]}
        with self.assertRaisesRegex(ScrapeError,"not supported"):
            parse_with_llm(session,cards)

    @patch("scraper.scrape.api_settings",return_value=("https://example.invalid/llm","fake","fake"))
    def test_llm_missing_records_fails(self,_):
        session=Mock()
        session.post.return_value.json.return_value={"choices":[{"message":{"content":json.dumps({"records":[]})}}]}
        with self.assertRaisesRegex(ScrapeError,"unexpected number"):
            parse_with_llm(session,collect_bonus_cards(HTML))

if __name__ == "__main__":
    unittest.main()
