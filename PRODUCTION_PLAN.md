# Production plan — 200 casinos, daily updates

For 200 casinos refreshed daily, I would host the public frontend on **Cloudflare Pages** and run a Python scraper in Docker on a small **DigitalOcean VPS**. Separating the site from data collection keeps pages fast, avoids scraping during user visits and protects credentials. Each source would have its own extraction rules, with robots.txt respected, rate limits and bounded retries.

I would store casinos, bonus terms, source URLs, collection timestamps and change history in **PostgreSQL**. Validated records would be exported as JSON for the website; failed runs would preserve the previous verified data. I would back up PostgreSQL nightly using `pg_dump` to separate S3-compatible storage, retain multiple restore points and test recovery periodically.

A **systemd timer** would schedule scraping daily. Logs and Sentry would capture errors, while a health-check alert would notify me if a run failed, fewer than expected casinos were updated, or the data became older than 26 hours.

I would buy a domain through a registrar and manage **DNS** with Cloudflare. Cloudflare Pages provides **HTTPS** for the public site, while the VPS would use a firewall, SSH keys and regular security updates.

For a small initial release I would budget around **US$15–35 per month**: VPS $6–12, backups $1–4, domain $1–2 monthly equivalent, AI requests $2–10, plus an allowance for monitoring and bandwidth. These are estimates, not provider quotes.
