# Approach and AI usage — developer assessment

## Short approach
I kept the solution small and auditable. Python checks robots.txt, retrieves one public comparison table and extracts three casino entries without typing bonus values into the program. I use a language model to extract the wagering multiplier from free-text terms, then validate it against source evidence before atomically saving the JSON; the other fields are extracted from the page. The responsive HTML/CSS/JavaScript page reads that JSON and provides simple search and sorting. Offline tests cover both valid extraction and failure cases.

## AI usage (five lines)
1. I used **ChatGPT** to assist with planning, code, frontend layout and unit tests; the running scraper uses local Qwen2.5-0.5B-Instruct (or OpenAI with an optional API key).
2. My original source, AskGamblers, redirected to a region-restricted page and was not reliable for the automation.
3. I caught this by checking the public URL and reviewing GitHub Actions instead of assuming it worked.
4. I switched to a publicly accessible comparison table, kept a strict robots.txt check and added source-grounded validation.
5. The original GitHub Models integration returned non-JSON text, so I switched to local Qwen. Its initial answer was 36 instead of the source's 6; validation caught it, and a few-shot prompt fixed the extraction.

## Actual elapsed time
**Just over 2 hours (estimated).** The assessment was completed within the 3-hour time cap.
