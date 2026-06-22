---
name: web-access-constraints
description: Known web-fetch limitations when researching Midjourney from this sandbox (Reddit blocked, docs.midjourney 403)
metadata:
  type: reference
---

When researching Midjourney (or anything) from this environment:

- **docs.midjourney.com returns HTTP 403** on direct WebFetch. Workaround: read the exact wording via WebSearch result snippets (the search tool surfaces verbatim doc sentences), or via credible secondary sources that quote the docs. This matches the note already in `docs/research/2026-05-11_.../06_moodboard-semantics-and-starter-recipe.md` frontmatter.
- **reddit.com is fully blocked**: WebSearch rejects `allowed_domains: ["reddit.com"]` (400 error), WebFetch on www.reddit.com fails ("unable to fetch"), the reddit `.json` API also fails, and Google/Bing/DuckDuckGo HTML-search proxies return only nav chrome, not thread bodies. Treat Reddit community sentiment as **not directly retrievable** — flag it as a gap rather than guessing.
- **updates.midjourney.com IS accessible** via WebFetch — this is the best authoritative source for version-specific (V8/V8.1) behavior claims.
- Substack posts often 301-redirect to a renamed host (e.g. nimblelab -> fabiomatoscruz); re-fetch the redirect target. Some Substack/Medium posts are paywalled mid-article.
