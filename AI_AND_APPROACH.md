# Approach and AI usage — developer assessment

## Short approach
I kept the solution small and auditable. Python checks robots.txt, retrieves one public comparison table and extracts three casino entries without typing bonus values into the program. I send the captured free-text terms to a language model, then check every returned field against the source text before atomically saving the JSON. The responsive HTML/CSS/JavaScript page reads that JSON and provides simple search and sorting. Offline tests cover both valid extraction and failure cases.

## AI usage (five lines)
1. I used **ChatGPT** to assist with planning, code, frontend layout and unit tests; the running scraper uses a model through OpenAI or GitHub Models.
2. My original source, AskGamblers, redirected to a region-restricted page and was not reliable for the automation.
3. I caught this by checking the public URL and reviewing GitHub Actions instead of assuming it worked.
4. I switched to a publicly accessible comparison table, kept a strict robots.txt check and added source-grounded validation.
5. GitHub Models initially returned non-parseable text; I added a JSON-only response requirement and tested the error path. Only claim the fix is fully working after a successful live run.

## Actual elapsed time
**To be filled in by the candidate.** The brief limits the assessment to three hours. The full implementation may exceed the brief's limit; be transparent with the reviewer if so, and do not misrepresent hours or unverified features.
