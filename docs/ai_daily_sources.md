# AI Daily Sources

Stage 4 keeps the AI daily report local-first and configurable. Sources live in
`config/ai_sources.yaml` instead of being hard-coded so the project can add,
disable, or replace feeds without changing collector code.

## Current RSS Sources

- OpenAI News: `https://openai.com/news/rss.xml`
- Google AI Blog: `https://blog.google/technology/ai/rss/`
- Google DeepMind News: `https://deepmind.google/blog/rss.xml`
- Hugging Face Blog: `https://huggingface.co/blog/feed.xml`

The RSS collector reads only sources where `enabled: true` and `type: rss`.
If a source fails, the collector logs a warning and continues with other
sources.

## Candidate Future Sources

- Anthropic News: useful for Claude and safety updates, but RSS availability can
  change; keep it as a future HTML collector candidate.
- Meta AI: useful for open model and research updates, but may need HTML parsing
  or another public feed.
- GitHub Trending / Releases: useful for developer tools and open-source AI
  projects, but the current Stage 4 implementation does not scrape HTML.

## Why Sources Are Configurable

- RSS URLs and site behavior change over time.
- Some sources are stable RSS feeds while others need future HTML collectors.
- Keeping categories in config lets the report renderer stay simple in Stage 4.
- Tests can use sample feeds without touching real networks or credentials.
