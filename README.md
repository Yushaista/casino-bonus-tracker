# BonusScope — casino bonus scraper and responsive comparison

A focused web-developer screening task. One Python command downloads public listing data for **three casinos**, asks an LLM to structure the bonus terms, validates the response and writes `data/bonuses.json`. A single static webpage displays the JSON without hardcoding bonus data into HTML or JavaScript.

**Chosen source:** [AskGamblers — South Africa Welcome Bonuses](https://www.askgamblers.com/casino-bonuses/countries/za/welcome). The script first checks `robots.txt`. If scraping is disallowed, redirected, unavailable or blocked, it exits without bypassing the restriction or rewriting old data. A change of source would require reviewing the extraction assumptions and tests.

## Install / run the scraper

Requirements: Python 3.10+ and an internet connection. On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY='your-api-key-here'
python -m scraper.scrape
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` and set the key using `$env:OPENAI_API_KEY='your-api-key-here'`. The **single scraping command** is `python -m scraper.scrape` after installation and configuration. The key is only used locally and must not be committed. Alternatively run the workflow in GitHub Actions, which uses its built-in `GITHUB_TOKEN` with `models: read` permission to call GitHub Models (subject to account availability and API limits).

When successful, the script prints `Saved 3 source-validated casinos...` and replaces `data/bonuses.json`. If unsuccessful, it prints the reason and leaves the old file unchanged. It makes only **one source-page request**, plus the robots check, and **one LLM request** for all three cards.

## Run the website

```bash
python -m http.server 8000
```

Open **http://localhost:8000**. Opening `index.html` directly via `file://` may prevent browser `fetch()` from reading the JSON. The page uses no frontend framework or build step.

## Run tests

```bash
python -m unittest discover -s tests -v
```

The tests run offline using a small HTML fixture and a mocked LLM response. They check complete-record selection, robots access restrictions, HTTP blocking and hallucinated wagering multipliers.

## Publish with GitHub Pages

1. Create a new GitHub repository, commit these files, and push to its `main` branch. Do **not** commit `.env` or any API key.
2. In **Settings → Pages**, choose **GitHub Actions** as the build/deployment source.
3. In **Actions → Test, refresh and deploy**, select **Run workflow** for a live scraping attempt. GitHub Models access must be available to your account; the workflow includes `models: read`.
4. Once the workflow succeeds, check `data/bonuses.json` has `"status": "live_scrape"`, exactly 3 casinos, and an actual `generated_at` timestamp. Review the Pages URL and test on a phone.
5. The workflow is also scheduled daily at 05:18 UTC. The script refuses disallowed or blocked access; if it fails, the workflow reports a failure without replacing the previous JSON.

> **Submission caveat:** The included `data/bonuses.json` is an **indexed-source preview** that was transcribed into structured data by ChatGPT from a publicly indexed page, *not* the output of a completed live scraper run. This preview exists for visual frontend review. **Do not submit it as proof that the scraper ran.** Replace it by running the actual command successfully before submission, or explicitly report the live integration as unfinished. If the source blocks the robot or changes structure, switch to a legitimately scrapable source and revise the parsing/tests rather than circumventing restrictions.

## Structure

- `scraper/scrape.py` — polite fetch, HTML listing extraction, LLM transformation, validation and atomic JSON write
- `data/bonuses.json` — the 3-record input for the public page (preview until refreshed)
- `index.html`, `assets/styles.css`, `assets/app.js` — responsive frontend; renders directly from JSON
- `tests/` — automated tests and test-only sample HTML
- `.github/workflows/website.yml` — scheduled refresh, test and GitHub Pages deployment
- `PRODUCTION_PLAN.md` — half-page scaling/ops/cost proposal
- `AI_AND_APPROACH.md` — approach, AI notes, and honest timing field

## Data integrity

The LLM extracts bonus copy, wagering multipliers and minimum deposit from captured source text, but a deterministic validation layer rejects invented values and inconsistent multipliers. `10xb` means wagering on bonus funds, while `7x(d+b)` means deposit plus bonus. This distinction is retained alongside the numeric multiplier. Casino bonus terms change; this is an informational technical exercise and not an endorsement. Always check the linked original terms. 18+.