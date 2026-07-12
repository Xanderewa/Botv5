import os
import time
import logging
from dataclasses import dataclass
from typing import List, Optional

import requests


@dataclass(frozen=True)
class Config:
    symbol: str = os.getenv("SYMBOL", "BTC-USDT")
    timeframe: str = os.getenv("TIMEFRAME", "15min")
    candles_limit: int = int(os.getenv("CANDLES_LIMIT", "50"))
    mode: str = os.getenv("MODE", "normal")

    kucoin_base_url: str = os.getenv("KUCOIN_BASE_URL", "https://api.kucoin.com")
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "10"))

    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    telegram_silent: bool = os.getenv("TELEGRAM_SILENT", "true").lower() == "true"

    run_forever: bool = os.getenv("RUN_FOREVER", "1") == "1"
    sleep_seconds: int = int(os.getenv("SLEEP_SECONDS", "60"))


@dataclass(frozen=True)
class Candle:
    ts: int
    open: float
    close: float
    high: float
    low: float
    volume: float
    turnover: float


def build_logger():
    logger = logging.getLogger("pro_signal_v3_min")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(h)
    return logger


def safe_float(value, default=0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def seconds_for_timeframe(timeframe: str) -> int:
    mapping = {
        "1min": 60,
        "3min": 180,
        "5min": 300,
        "15min": 900,
        "30min": 1800,
        "1hour": 3600,
        "2hour": 7200,
        "4hour": 14400,
        "6hour": 21600,
        "8hour": 28800,
        "12hour": 43200,
        "1day": 86400,
    }
    return mapping.get(timeframe, 900)


def fetch_candles(cfg: Config) -> List[Candle]:
    end_at = int(time.time())
    start_at = end_at - seconds_for_timeframe(cfg.timeframe) * cfg.candles_limit
    url = f"{cfg.kucoin_base_url.rstrip('/')}/api/v1/market/candles"
    params = {
        "symbol": cfg.symbol,
        "type": cfg.timeframe,
        "startAt": start_at,
        "endAt": end_at,
    }
    r = requests.get(url, params=params, timeout=cfg.request_timeout)
    r.raise_for_status()
    payload = r.json()
    data = payload.get("data") or []
    candles = []
    for row in reversed(data):
        candles.append(
            Candle(
                ts=int(row[0]),
                open=safe_float(row[1]),
                close=safe_float(row[2]),
                high=safe_float(row[3]),
                low=safe_float(row[4]),
                volume=safe_float(row[5]),
                turnover=safe_float(row[6]) if len(row) > 6 else 0.0,
            )
        )
    return candles


def ema(values: List[float], period: int) -> Optional[float]:
    if len(values) < period:
        return None
    k = 2 / (period + 1)
    current = sum(values[:period]) / period
    for price in values[period:]:
        current = (price - current) * k + current
    return current


def send_telegram(cfg: Config, text: str) -> bool:
    if not cfg.telegram_bot_token or not cfg.telegram_chat_id:
        return False
    url = f"https://api.telegram.org/bot{cfg.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": cfg.telegram_chat_id,
        "text": text,
        "disable_notification": cfg.telegram_silent,
    }
    r = requests.post(url, data=payload, timeout=cfg.request_timeout)
    r.raise_for_status()
    return True


def build_message(cfg: Config, candles: List[Candle]) -> str:
    last = candles[-1]
    closes = [c.close for c in candles]
    fast = ema(closes, 9)
    slow = ema(closes, 21)

    if fast is None or slow is None:
        return f"{cfg.symbol} | datos insuficientes | close={last.close:.2f}"

    if fast > slow:
        direction = "LONG"
    elif fast < slow:
        direction = "SHORT"
    else:
        direction = "NEUTRAL"

    return (
        f"{cfg.symbol} | {direction} | {cfg.mode}
"
        f"Precio: {last.close:.2f}
"
        f"EMA9: {fast:.2f}
"
        f"EMA21: {slow:.2f}"
    )


def main():
    cfg = Config()
    logger = build_logger()

    logger.info("iniciando bot mínimo")
    logger.info(f"symbol={cfg.symbol} timeframe={cfg.timeframe} mode={cfg.mode}")

    while True:
        try:
            candles = fetch_candles(cfg)
            if not candles:
                logger.warning("sin datos de KuCoin")
            else:
                msg = build_message(cfg, candles)
                logger.info(msg.replace("
", " | "))
                sent = send_telegram(cfg, msg)
                logger.info(f"telegram_sent={sent}")
        except Exception as e:
            logger.exception(f"error: {e}")

        if not cfg.run_forever:
            break
        time.sleep(cfg.sleep_seconds)


if __name__ == "__main__":
    main()