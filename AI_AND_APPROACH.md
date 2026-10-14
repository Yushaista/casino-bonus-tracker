# Approach and AI usage — developer assessment

## Short approach
I kept the solution small and auditable. Python checks robots.txt, retrieves one public comparison table and extracts three casino entries without typing bonus values into the program. I send the captured free-text terms to a language model, then check every returned field against the source text before atomically saving the JSON. The responsive HTML/CSS/JavaScript page reads that JSON and provides simple search and sorting. Offline tests cover both valid extraction and failure cases.

## AI usage (five lines)
1. I used **ChatGPT** to assist with planning, code, frontend layout and unit tests; the running scraper uses local FLAN-T5 (or OpenAI with an optional API key).
2. My original source, AskGamblers, redirected to a region-restricted page and was not reliable for the automation.
3. I caught this by checking the public URL and reviewing GitHub Actions instead of assuming it worked.
4. I switched to a publicly accessible comparison table, kept a strict robots.txt check and added source-grounded validation.
5. The original integration attempted the retired local FLAN-T5 API; its response was not JSON. I identified this in the CI logs and replaced it with an open-weight local language model. I validate the model's numeric answer against the source.

## Actual elapsed time
**To be filled in by the candidate.** The brief limits the assessment to three hours. The full implementation may exceed the brief's limit; be transparent with the reviewer if so, and do not misrepresent hours or unverified features.
