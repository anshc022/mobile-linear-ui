# OpenWork Auto-Submission Bot

A Node.js bot that automatically fetches, filters, and submits to OpenWork bounties.

## Features

- **Job Fetching** — Pulls open jobs from the OpenWork API
- **Smart Filtering** — Filter by minimum reward, tags, and exclude tags
- **Template Engine** — Configurable submission templates with variable interpolation
- **Rate Limiting** — Respects API limits (configurable, default 10/hr)
- **Retry Logic** — Exponential backoff with configurable retry count
- **State Persistence** — Tracks submitted jobs to avoid duplicates
- **Comprehensive Logging** — File + console logging with configurable levels
- **Dry Run Mode** — Preview what would be submitted without actually submitting

## Requirements

- Node.js >= 18.0.0 (uses native `fetch`)

## Setup

```bash
# 1. Configure
cp config.json config.json  # edit with your API key and preferences

# 2. Run
node index.js

# 3. Or dry-run first
node index.js --dry-run
```

## Configuration

Edit `config.json`:

| Field | Description |
|-------|-------------|
| `apiKey` | Your OpenWork API key |
| `apiBaseUrl` | API base URL |
| `filters.minReward` | Minimum reward threshold |
| `filters.tags` | Only submit to jobs with these tags (empty = all) |
| `filters.excludeTags` | Skip jobs with these tags |
| `filters.maxSubmissionsPerHour` | Rate limit (default: 10) |
| `templates.*` | Submission templates with `{variable}` placeholders |
| `retryPolicy.maxRetries` | Max retry attempts on failure |
| `retryPolicy.backoffMs` | Initial backoff delay |

## Architecture

```
index.js
├── Logger          — Structured file + console logging
├── RateLimiter     — Sliding window rate limiter
├── OpenWorkClient  — API client with retry logic
├── Template Engine — Variable interpolation for submissions
├── Filter Engine   — Tag/reward matching
└── State Manager   — JSON-based deduplication
```

## Files

- `config.json` — Configuration
- `activity.log` — Runtime logs (auto-created)
- `.state.json` — Submission state (auto-created)

## License

MIT
