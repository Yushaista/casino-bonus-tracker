# BonusScope — casino bonus scraper + responsive comparison

A focused end-to-end developer screening project: **one command**, one public data source, **three casinos**, AI-assisted extraction, a validated JSON file, and one deployed mobile-friendly page.

**Live page:** https://yushaista.github.io/casino-bonus-tracker/  
**Alternate Vercel page:** https://casino-bonus-tracker.vercel.app/  
**Repository:** https://github.com/Yushaista/casino-bonus-tracker  
**Source:** https://betproof.co.za/casino-bonuses-south-africa/

## What it demonstrates

- Scraper retrieves the public BetProof comparison table for PlayaBets, Springbok Casino, and Thunderbolt Casino.
- Extracts **welcome bonus**, **wagering multiplier**, **minimum deposit**, and **source URL**, retaining the source wording and wager basis where known.
- Uses a small **local instruction-following language model** (Qwen2.5-0.5B-Instruct) to extract the wagering multiplier from the captured free-text offer; it validates the model's answer against the source. Other displayed fields are parsed directly from the source.
- Checks `robots.txt` first. Does not follow blocked redirects or bypass CAPTCHAs/logins. If the source is disallowed or unavailable, **fails without modifying the last valid JSON**.
- Writes `data/bonuses.json` atomically only after all three offers validate.
- Static website reads **the JSON**, not hardcoded values. Responsive table/cards, search, sort, reload button, loading/empty/error states, timestamps, and accessible source links.
- GitHub Actions tests every push and attempts a fresh scrape with a local model automatically and daily at **05:18 UTC**; a successful result is committed, triggering Vercel redeployment; GitHub Pages is also published.

## Install / run (Python 3.10+)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install torch --index-url https://download.pytorch.org/whl/cpu  # optional CPU-only install
pip install -r requirements.txt
python -m scraper.scrape
```

**Single scrape command:** `python -m scraper.scrape`. By default the script downloads and runs the open-weight `Qwen/Qwen2.5-0.5B-Instruct` language model on your machine or CI runner (no API key required). The first run needs internet access to fetch weights. Setting `OPENAI_API_KEY` optionally chooses hosted OpenAI instead. Never commit API keys. Expect output `Saved 3...` on success.

## Run website locally

```bash
python -m http.server 8000
```

Open http://localhost:8000 (rather than `file://`, which may block JSON fetching).

## Run tests

```bash
python -m unittest discover -s tests -v
```

Ten offline unit tests verify source table extraction, unknown/ambiguous data rejection, robots access restrictions, redirects, and LLM hallucination/record count validation. These tests **do not replace** a successful live integration run.

## Data integrity / runtime status

Look at `data/bonuses.json`:
- `status: "live_scrape"` + valid `generated_at` + **3 records** = output from a successful source and model run.
- `status: "pending_scrape"` = no validated live snapshot yet; the site deliberately displays **no invented records**.
- On any scrape/LLM/validation error the script exits nonzero and **preserves the last valid file**.

The source's `6x` and `30x` figures do **not** necessarily specify whether the wager applies to bonus, deposit, or both. This is kept as `wagering_basis: "unspecified"` rather than inferred. Source terms can change and may include additional restrictions. This is a technical assessment, not a casino recommendation. 18+.

## Files

- `scraper/scrape.py`: robots-checking fetch, table extraction, AI parsing, source validation, atomic JSON write.
- `data/bonuses.json`: generated records from the last verified scrape.
- `index.html`, `assets/`: static, dependency-free responsive frontend and working controls.
- `tests/`: offline unit tests and an illustrative HTML table fixture.
- `.github/workflows/website.yml`: tests, daily/source refresh and Git commit.
- `PRODUCTION_PLAN.md`: scaling proposal for 200 casinos (hosting, DB, backups, DNS/HTTPS, schedule, monitoring, costs).
- `AI_AND_APPROACH.md`: personal approach, five lines about AI, and time-tracking field.

## Deployment

The GitHub Pages workflow publishes the responsive page directly; Vercel is also connected to `main`. Pushes trigger deployments. GitHub Actions runs on pushes and daily. It downloads a local model, and may fail if the source blocks automated access or if model extraction fails strict checks. Check the latest workflow **and the current JSON status** before claiming the full integration is live.
