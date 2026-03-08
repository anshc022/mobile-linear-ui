# SOL Price Alert Bot

A Python bot that monitors Solana's price via CoinGecko and alerts when configurable thresholds are crossed.

## Features

- **Real-time Monitoring** — Polls CoinGecko API at configurable intervals
- **Flexible Thresholds** — Set multiple above/below price triggers with custom messages
- **Alert Cooldowns** — Prevents spam with per-threshold cooldown timers
- **Webhook Support** — Optional webhook notifications (Slack, Discord, etc.)
- **Comprehensive Logging** — File + console with configurable log levels
- **Graceful Shutdown** — Clean exit on Ctrl+C
- **Single Check Mode** — Run once with `--once` flag

## Requirements

- Python >= 3.10
- `requests` library

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure thresholds
# Edit config.json with your desired price thresholds

# 3. Run
python price_alert.py

# Or single check
python price_alert.py --once
```

## Configuration

Edit `config.json`:

| Field | Description |
|-------|-------------|
| `coin` | CoinGecko coin ID (default: `solana`) |
| `currency` | Fiat currency (default: `usd`) |
| `checkIntervalSeconds` | Polling interval |
| `thresholds` | Array of `{type, price, message}` objects |
| `alertCooldownMinutes` | Minutes before re-triggering same threshold |
| `webhook.enabled` | Enable webhook notifications |
| `webhook.url` | Webhook endpoint URL |
| `logging.file` | Log file path |
| `logging.level` | Log level (DEBUG/INFO/WARNING/ERROR) |

### Threshold Types

- `above` — Triggers when price goes above the specified value
- `below` — Triggers when price drops below the specified value

## Architecture

```
price_alert.py
├── load_config()    — JSON config loader with validation
├── fetch_price()    — CoinGecko API client
├── AlertEngine      — Threshold checker with cooldown management
├── send_alert()     — Alert dispatcher (console + webhook)
└── run()            — Main monitoring loop
```

## License

MIT
