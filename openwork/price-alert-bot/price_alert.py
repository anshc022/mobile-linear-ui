#!/usr/bin/env python3
"""
SOL Price Alert Bot

Monitors Solana price via CoinGecko API and sends alerts
when configurable thresholds are crossed.
"""

import json
import logging
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests

# ── Configuration ────────────────────────────────────────────────────────────

CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config(path: Path = CONFIG_PATH) -> dict:
    """Load and validate configuration from JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path) as f:
        config = json.load(f)
    required = ["coin", "currency", "checkIntervalSeconds", "thresholds"]
    for key in required:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    return config


# ── Logger ───────────────────────────────────────────────────────────────────


def setup_logger(config: dict) -> logging.Logger:
    """Configure logging to file and console."""
    log_config = config.get("logging", {})
    level = getattr(logging, log_config.get("level", "INFO").upper(), logging.INFO)

    logger = logging.getLogger("price_alert")
    logger.setLevel(level)
    logger.handlers.clear()

    fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")

    # Console
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # File
    log_file = log_config.get("file")
    if log_file:
        fh = logging.FileHandler(Path(__file__).parent / log_file)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


# ── Price Fetcher ────────────────────────────────────────────────────────────

COINGECKO_API = "https://api.coingecko.com/api/v3"


def fetch_price(coin: str, currency: str, logger: logging.Logger) -> float | None:
    """Fetch current price from CoinGecko. Returns None on failure."""
    url = f"{COINGECKO_API}/simple/price"
    params = {"ids": coin, "vs_currencies": currency}
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        price = data.get(coin, {}).get(currency)
        if price is None:
            logger.error(f"Unexpected response structure: {data}")
        return price
    except requests.RequestException as e:
        logger.error(f"Failed to fetch price: {e}")
        return None


# ── Alert Engine ─────────────────────────────────────────────────────────────


class AlertEngine:
    """Manages threshold checking and alert cooldowns."""

    def __init__(self, thresholds: list[dict], cooldown_minutes: int, logger: logging.Logger):
        self.thresholds = thresholds
        self.cooldown = timedelta(minutes=cooldown_minutes)
        self.logger = logger
        self.last_alerted: dict[str, datetime] = {}

    def _threshold_key(self, threshold: dict) -> str:
        return f"{threshold['type']}_{threshold['price']}"

    def check(self, price: float) -> list[dict]:
        """Check price against thresholds. Returns list of triggered alerts."""
        triggered = []
        now = datetime.now()

        for t in self.thresholds:
            key = self._threshold_key(t)
            match = (
                (t["type"] == "above" and price > t["price"]) or
                (t["type"] == "below" and price < t["price"])
            )
            if not match:
                continue

            last = self.last_alerted.get(key)
            if last and (now - last) < self.cooldown:
                self.logger.debug(f"Cooldown active for {key}, skipping")
                continue

            self.last_alerted[key] = now
            triggered.append(t)

        return triggered


# ── Notification ─────────────────────────────────────────────────────────────


def send_webhook(url: str, method: str, message: str, price: float, logger: logging.Logger):
    """Send alert via webhook."""
    payload = {
        "text": message,
        "price": price,
        "timestamp": datetime.now().isoformat(),
    }
    try:
        resp = requests.request(method, url, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info(f"Webhook sent successfully")
    except requests.RequestException as e:
        logger.error(f"Webhook failed: {e}")


def send_alert(alert: dict, price: float, config: dict, logger: logging.Logger):
    """Dispatch an alert through configured channels."""
    message = alert.get("message", f"SOL price alert: ${price}")
    logger.warning(f"🚨 ALERT: {message} (current: ${price:.2f})")

    webhook = config.get("webhook", {})
    if webhook.get("enabled") and webhook.get("url"):
        send_webhook(webhook["url"], webhook.get("method", "POST"), message, price, logger)


# ── Main Loop ────────────────────────────────────────────────────────────────


def run(config: dict, logger: logging.Logger, single_check: bool = False):
    """Main monitoring loop."""
    coin = config["coin"]
    currency = config["currency"]
    interval = config["checkIntervalSeconds"]
    cooldown = config.get("alertCooldownMinutes", 30)

    engine = AlertEngine(config["thresholds"], cooldown, logger)
    logger.info(f"Monitoring {coin.upper()} in {currency.upper()}, interval={interval}s, thresholds={len(config['thresholds'])}")

    while True:
        price = fetch_price(coin, currency, logger)

        if price is not None:
            logger.info(f"{coin.upper()} = ${price:,.2f} {currency.upper()}")
            triggered = engine.check(price)
            for alert in triggered:
                send_alert(alert, price, config, logger)
        else:
            logger.warning("Price fetch failed, will retry next cycle")

        if single_check:
            return price

        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Shutting down gracefully")
            break


def main():
    config = load_config()
    logger = setup_logger(config)
    single = "--once" in sys.argv
    run(config, logger, single_check=single)


if __name__ == "__main__":
    main()
