"""Mocked tests: no live web requests or model API charges."""
import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from scraper.scrape import ScrapeError, collect_bonus_cards, fetch_page, parse_with_llm

HTML = (Path(__file__).parent / 'fixtures/listing.html').read_text(encoding='utf-8')

class ScraperTests(unittest.TestCase):
    def test_three_complete_cards_and_skips_missing_wagering(self):
        cards = collect_bonus_cards(HTML)
        self.assertEqual([c['casino'] for c in cards], ['Jackpot City Casino', 'YesPlay Casino', 'BetBay Casino'])

    def test_missing_cards_raise_instead_of_fabricating(self):
        with self.assertRaises(ScrapeError):
            collect_bonus_cards('<html><body>No offers</body></html>')

    def test_robots_blocks_page(self):
        session = Mock()
        session.get.return_value = Mock(status_code=200, text='User-agent: *\nDisallow: /casino-bonuses/')
        with self.assertRaisesRegex(ScrapeError, 'disallows'):
            fetch_page(session)
        self.assertEqual(session.get.call_count, 1)

    def test_blocked_source_stops_without_bypass(self):
        session = Mock()
        session.get.side_effect = [Mock(status_code=404), Mock(status_code=403)]
        with self.assertRaisesRegex(ScrapeError, '403'):
            fetch_page(session)

    @patch('scraper.scrape.api_settings', return_value=('https://example.invalid/llm', 'fake', 'fake-model'))
    def test_llm_checks_reject_unsourced_multiplier(self, _settings):
        cards = collect_bonus_cards(HTML)
        values = [
            {'casino': 'Jackpot City Casino','welcome_bonus':'100% up to 4000 ZAR','wagering_raw':'10xb','wagering_multiplier':10,'wagering_basis':'bonus','minimum_deposit':'50 ZAR'},
            {'casino': 'YesPlay Casino','welcome_bonus':'100% up to 3000 ZAR','wagering_raw':'7x(d+b)','wagering_multiplier':7,'wagering_basis':'deposit_plus_bonus','minimum_deposit':'20 ZAR'},
            {'casino': 'BetBay Casino','welcome_bonus':'350% up to €2000 + 1000 Free Spins, Welcome Package at BetBay Casino','wagering_raw':'30x(d+b)','wagering_multiplier':30,'wagering_basis':'deposit_plus_bonus','minimum_deposit':'€25'}
        ]
        session = Mock()
        session.post.return_value.json.return_value = {'choices':[{'message':{'content':json.dumps({'records':values})}}]}
        result = parse_with_llm(session,cards)
        self.assertEqual(len(result),3)
        self.assertEqual(result[1]['wagering_basis'],'deposit_plus_bonus')
        values[0]['wagering_multiplier']=1000
        session.post.return_value.json.return_value = {'choices':[{'message':{'content':json.dumps({'records':values})}}]}
        with self.assertRaisesRegex(ScrapeError,'differs from source'):
            parse_with_llm(session,cards)

if __name__ == '__main__':
    unittest.main()
