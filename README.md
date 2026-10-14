# BonusScope — casino bonus scraper + responsive comparison

A focused end-to-end developer screening project: **one command**, one public data source, **three casinos**, AI-assisted extraction, a validated JSON file, and one deployed mobile-friendly page.

**Live page:** https://casino-bonus-tracker.vercel.app/  
**Repository:** https://github.com/Yushaista/casino-bonus-tracker  
**Source:** https://betproof.co.za/casino-bonuses-south-africa/

## What it demonstrates

- Scraper retrieves the public BetProof comparison table for PlayaBets, Springbok Casino, and Thunderbolt Casino.
- Extracts **welcome bonus**, **wagering multiplier**, **minimum deposit**, and **source URL**, retaining the source wording and wager basis where known.
- Sends each captured free-text offer to a language model to structure the fields; then rejects any AI-generated field not supported by the source.
- Checks `robots.txt` first. Does not follow blocked redirects or bypass CAPTCHAs/logins. If the source is disallowed or unavailable, **fails without modifying the last valid JSON**.
- Writes `data/bonuses.json` atomically only after all three offers validate.
- Static website reads **the JSON**, not hardcoded values. Responsive table/cards, search, sort, reload button, loading/empty/error states, timestamps, and accessible source links.
- GitHub Actions tests every push and attempts a fresh scrape automatically and daily at **05:18 UTC**; a successful result is committed, triggering Vercel redeployment.

## Install / run (Python 3.10+)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"  # Windows PowerShell: $env:OPENAI_API_KEY="your-key"
python -m scraper.scrape
```

**Single scrape command:** `python -m scraper.scrape`. The script uses a local `OPENAI_API_KEY`, or `GITHUB_TOKEN` when run in GitHub Actions with `models: read` permission. No API keys are stored in the repository. Both network access and model access are required. Expect output `Saved 3...` on success.

## Run website locally

```bash
python -m http.server 8000
```

Open http://localhost:8000 (rather than `file://`, which may block JSON fetching).

## Run tests

```bash
python -m unittest discover -s tests -v
```

Eight mocked tests verify source table extraction, unknown/ambiguous data rejection, robots access restrictions, redirects, and LLM hallucination/record count validation. These tests **do not replace** a successful live integration run.

## Data integrity / runtime status

Look at `data/bonuses.json`:
- `status: "live_scrape"` + valid `generated_at` + **3 records** = output from a successful source and model run.
- `status: "pending_scrape"` = no validated live snapshot yet; the site deliberately displays **no invented records**.
- On any scrape/LLM/validation error the script exits nonzero and **preserves the last valid file**.

The source's `6x` and `30x` figures do **not** necessarily specify whether the wager applies to bonus, deposit, or both. This is kept as `wagering_basis: "unspecified"` rather than inferred. Source terms can change and may include additional restrictions. This is a technical assessment, not a casino recommendation. 18+.

## Files

- `scraper/scrape.py`: robots-checking fetch, table extraction, AI parsing, source validation, atomic JSON write.
- `data/bonuses.json`: actual website data, initially empty until a successful scrape.
- `index.html`, `assets/`: static, dependency-free responsive frontend and working controls.
- `tests/`: offline unit tests and an illustrative HTML table fixture.
- `.github/workflows/website.yml`: tests, daily/source refresh and Git commit.
- `PRODUCTION_PLAN.md`: scaling proposal for 200 casinos (hosting, DB, backups, DNS/HTTPS, schedule, monitoring, costs).
- `AI_AND_APPROACH.md`: personal approach, five lines about AI, and time-tracking field.

## Deployment

The Vercel project is connected to the repository's `main` branch. Pushes trigger deployments. GitHub Actions runs on pushes and daily, and may fail if a website blocks automated access or GitHub Models returns invalid output. Check the latest workflow **and the current JSON status** before claiming the full integration is live.
