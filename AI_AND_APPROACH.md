# Approach and AI usage notes

## Brief approach
I kept the take-home intentionally small: Python retrieves the listing once, after checking robots.txt. BeautifulSoup identifies three complete bonus cards. A language model turns those cards into structured values, including the wagering multiplier and its calculation basis. Each extracted value is checked against the actual source text before the JSON is atomically replaced. A dependency-free JavaScript page reads the JSON and adapts the table to mobile screens. Tests cover source changes, access blocks and incorrect AI results. This is a practical demonstration, not a gambling recommendation.

## AI notes (five lines)
1. Tool used: **ChatGPT** to help plan and implement the Python and frontend code; the running scraper uses **GPT-4o-mini** via OpenAI or GitHub Models.
2. ChatGPT initially identified a public comparison page before verifying that automated scraping was permitted.
3. I caught the gap when robots.txt could not be inspected from this restricted development environment.
4. I corrected the approach by making the scraper check robots.txt itself and stop safely if it is disallowed or cannot be verified.
5. I also added validation to prevent the language model treating `10xb` and `7x(d+b)` as equivalent wagering conditions.

## Time spent
**Fill this in with your real elapsed work time before submitting.** The employer caps the assessment at 3 hours. Do not claim the unavailable live integration or deployment is complete until it has been tested.
