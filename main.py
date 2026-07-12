import os
import time
import json
import hashlib
import logging
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass(frozen=True)
class Config:
    symbol: str = os.getenv("SYMBOL", "BTC-USDT")
    timeframe: str = os.getenv("TIMEFRAME", "15min")
    candles_limit: int = int(os.getenv("CANDLES_LIMIT", "120"))
    mode: str = os.getenv("MODE", "normal")

    ema_fast: int = int(os.getenv("EMA_FAST", "9"))
    ema_slow: int = int(os.getenv("EMA_SLOW", "21"))
    rsi_period: int = int(os.getenv("RSI_PERIOD", "14"))
    atr_period: int = int(os.getenv("ATR_PERIOD", "14"))
    volume_period: int = int(os.getenv("VOLUME_PERIOD", "20"))

    cooldown_bars: int = int(os.getenv("COOLDOWN_BARS", "6"))
    prealert_ttl_bars: int = int(os.getenv("PREALERT_TTL_BARS", "3"))
    max_history: int = int(os.getenv("MAX_HISTORY", "25"))

    kucoin_base_url: str = os.getenv("KUCOIN_BASE_URL", "https://api.kucoin.com")
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
    request_timeout_read: int = int(os.getenv("REQUEST_TIMEOUT_READ", "15"))
    request_retries: int = int(os.getenv("REQUEST_RETRIES", "3"))

    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    telegram_parse_mode: str = os.getenv("TELEGRAM_PARSE_MODE", "HTML")
    telegram_silent: bool = os.getenv("TELEGRAM_SILENT", "true").lower() == "true"

    state_file: str = os.getenv("STATE_FILE", "pro_signal_state.json")
    log_level: int = logging.INFO


@dataclass(frozen=True)
class Candle:
    ts: int
    open: float
    close: float
    high: float
    low: float
    volume: float
    turnover: float


@dataclass
class StrategyDecision:
    direction: str
    mode: str
    reason: str
    confidence: float
    validations_passed: List[str] = field(default_factory=list)
    validations_failed: List[str] = field(default_factory=list)
    should_prealert: bool = False
    should_confirm: bool = False
    price: float = 0.0
    rsi: float = 0.0
    volume_state: str = "unknown"
    volatility_state: str = "unknown"
    context_hash: str = ""


@dataclass
class ManagerDecision:
    state: str
    reason: str
    send_message: bool
    message_type: str


@dataclass
class SignalState:
    last_context_hash: str = ""
    last_direction: str = ""
    last_candle_ts: int = 0
    cooldown_until_ts: int = 0
    prealert_expiry_ts: int = 0
    active: bool = False
    last_signal_type: str = ""
    history: List[Dict[str, Any]] = field(default_factory=list)


class StateStore:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> SignalState:
        if not os.path.exists(self.path):
            return SignalState()
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            return SignalState(**raw)
        except Exception:
            return SignalState()

    def save(self, state: SignalState) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(asdict(state), f, ensure_ascii=False, indent=2)
        except Exception:
            pass


class KucoinClient:
    def __init__(self, base_url: str, timeout: int = 10, read_timeout: int = 15, retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.timeout = (timeout, read_timeout)
        self.session = requests.Session()
        retry = Retry(
            total=retries,
            backoff_factor=0.8,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET"]),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get_candles(self, symbol: str, timeframe: str, limit: int = 120) -> List[Candle]:
        end_at = int(time.time())
        start_at = end_at - seconds_for_timeframe(timeframe) * limit
        url = f"{self.base_url}/api/v1/market/candles"
        params = {"symbol": symbol, "type": timeframe, "startAt": start_at, "endAt": end_at}
        r = self.session.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        payload = r.json() if r.content else {}
        data = payload.get("data") or []
        if not data:
            return []
        candles: List[Candle] = []
        for row in reversed(data):
            candles.append(Candle(
                ts=int(row[0]),
                open=safe_float(row[1]),
                close=safe_float(row[2]),
                high=safe_float(row[3]),
                low=safe_float(row[4]),
                volume=safe_float(row[5]),
                turnover=safe_float(row[6]) if len(row) > 6 else 0.0,
            ))
        return candles


class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str, parse_mode: str = "HTML", silent: bool = True):
        self.bot_token = bot_token.strip()
        self.chat_id = chat_id.strip()
        self.parse_mode = parse_mode
        self.silent = silent

    def send(self, text: str) -> bool:
        if not self.bot_token or not self.chat_id:
            return False
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": self.parse_mode,
            "disable_notification": self.silent,
        }
        r = requests.post(url, data=payload, timeout=(10, 15))
        r.raise_for_status()
        return True


class BotLogger:
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger("pro_signal_v3")
        if not self.logger.handlers:
            self.logger.setLevel(level)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            self.logger.addHandler(handler)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def exception(self, msg: str):
        self.logger.exception(msg)


def safe_float(value, default=0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def seconds_for_timeframe(timeframe: str) -> int:
    mapping = {
        "1min": 60, "3min": 180, "5min": 300, "15min": 900, "30min": 1800,
        "1hour": 3600, "2hour": 7200, "4hour": 14400, "6hour": 21600,
        "8hour": 28800, "12hour": 43200, "1day": 86400, "1week": 604800,
        "1month": 2592000,
    }
    return mapping.get(timeframe, 900)


def mode_thresholds(mode: str) -> Dict[str, float]:
    if mode == "aggressive":
        return {"rsi_long": 50, "rsi_short": 50, "volume_mult": 0.95, "volatility_min": 0.0020, "min_confidence": 0.55}
    if mode == "passive":
        return {"rsi_long": 55, "rsi_short": 45, "volume_mult": 1.10, "volatility_min": 0.0040, "min_confidence": 0.80}
    return {"rsi_long": 52, "rsi_short": 48, "volume_mult": 1.00, "volatility_min": 0.0030, "min_confidence": 0.68}


def ema(values: List[float], period: int) -> List[float]:
    if len(values) < period:
        return []
    k = 2 / (period + 1)
    out = [sum(values[:period]) / period]
    for price in values[period:]:
        out.append((price - out[-1]) * k + out[-1])
    return out


def rsi(values: List[float], period: int = 14) -> Optional[float]:
    if len(values) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(values)):
        diff = values[i] - values[i - 1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def atr(candles: List[Candle], period: int = 14) -> Optional[float]:
    if len(candles) < period + 1:
        return None
    trs = []
    for i in range(1, len(candles)):
        c, p = candles[i], candles[i - 1]
        trs.append(max(c.high - c.low, abs(c.high - p.close), abs(c.low - p.close)))
    return sum(trs[-period:]) / period


def volume_mean(candles: List[Candle], period: int = 20) -> Optional[float]:
    if len(candles) < period:
        return None
    return sum(c.volume for c in candles[-period:]) / period


def market_context_hash(candles: List[Candle], decision: StrategyDecision) -> str:
    last = candles[-1]
    raw = f"{decision.direction}|{decision.mode}|{decision.reason}|{last.close:.2f}|{last.ts}|{decision.confidence:.2f}"
    return hashlib.sha256(raw.encode()).hexdigest()


class StrategyEngine:
    def evaluate(self, candles: List[Candle], mode: str, cfg: Config) -> StrategyDecision:
        closes = [c.close for c in candles]
        fast = ema(closes, cfg.ema_fast)
        slow = ema(closes, cfg.ema_slow)
        current_rsi = rsi(closes, cfg.rsi_period)
        current_atr = atr(candles, cfg.atr_period)
        avg_volume = volume_mean(candles, cfg.volume_period)

        if not fast or not slow or current_rsi is None or current_atr is None or avg_volume is None:
            return StrategyDecision(direction="NONE", mode=mode, reason="insufficient_data", confidence=0.0, validations_failed=["insufficient_data"])

        last_close = closes[-1]
        ema_fast_last = fast[-1]
        ema_slow_last = slow[-1]
        last_volume = candles[-1].volume
        thresholds = mode_thresholds(mode)

        volume_ok = last_volume >= avg_volume * thresholds["volume_mult"]
        volatility_ratio = current_atr / last_close if last_close else 0.0
        volatility_ok = volatility_ratio >= thresholds["volatility_min"]

        validations_passed, validations_failed = [], []
        if ema_fast_last > ema_slow_last:
            validations_passed.append("ema_bull")
        else:
            validations_failed.append("ema_bull")
        if ema_fast_last < ema_slow_last:
            validations_passed.append("ema_bear")
        else:
            validations_failed.append("ema_bear")
        if volume_ok:
            validations_passed.append("volume_ok")
        else:
            validations_failed.append("volume_ok")
        if volatility_ok:
            validations_passed.append("volatility_ok")
        else:
            validations_failed.append("volatility_ok")

        long_ok = ema_fast_last > ema_slow_last and current_rsi >= thresholds["rsi_long"]
        short_ok = ema_fast_last < ema_slow_last and current_rsi <= thresholds["rsi_short"]

        if long_ok and volume_ok and volatility_ok:
            return StrategyDecision(
                direction="LONG",
                mode=mode,
                reason="RSI válido + EMA alineadas + volumen suficiente",
                confidence=thresholds["min_confidence"] + 0.07,
                validations_passed=validations_passed + ["rsi_long"],
                validations_failed=validations_failed,
                should_prealert=(mode == "aggressive"),
                should_confirm=True,
                price=last_close,
                rsi=current_rsi,
                volume_state="high",
                volatility_state="useful",
            )

        if short_ok and volume_ok and volatility_ok:
            return StrategyDecision(
                direction="SHORT",
                mode=mode,
                reason="RSI válido + EMA alineadas + volumen suficiente",
                confidence=thresholds["min_confidence"] + 0.07,
                validations_passed=validations_passed + ["rsi_short"],
                validations_failed=validations_failed,
                should_prealert=(mode == "aggressive"),
                should_confirm=True,
                price=last_close,
                rsi=current_rsi,
                volume_state="high",
                volatility_state="useful",
            )

        if mode == "aggressive" and volume_ok and volatility_ok:
            return StrategyDecision(
                direction="PREALERT",
                mode=mode,
                reason="posible ruptura en curso",
                confidence=0.56,
                validations_passed=validations_passed,
                validations_failed=validations_failed,
                should_prealert=True,
                should_confirm=False,
                price=last_close,
                rsi=current_rsi,
                volume_state="high" if volume_ok else "low",
                volatility_state="useful" if volatility_ok else "weak",
            )

        return StrategyDecision(
            direction="NONE",
            mode=mode,
            reason="no_setup",
            confidence=0.0,
            validations_passed=validations_passed,
            validations_failed=validations_failed,
            price=last_close,
            rsi=current_rsi,
            volume_state="high" if volume_ok else "low",
            volatility_state="useful" if volatility_ok else "weak",
        )


class SignalManager:
    def __init__(self, cfg: Config, store: StateStore):
        self.cfg = cfg
        self.store = store
        self.state = store.load()

    def evaluate(self, decision: StrategyDecision, candles: List[Candle]) -> ManagerDecision:
        last_ts = candles[-1].ts
        ctx = market_context_hash(candles, decision)

        if last_ts <= self.state.last_candle_ts:
            return ManagerDecision("blocked", "same_candle", False, "blocked")
        if self.state.cooldown_until_ts and last_ts < self.state.cooldown_until_ts:
            return ManagerDecision("cooldown", "recent_signal", False, "cooldown")
        if ctx == self.state.last_context_hash:
            return ManagerDecision("blocked", "same_context", False, "blocked")

        if decision.should_confirm and decision.direction in {"LONG", "SHORT"}:
            self.state.last_context_hash = ctx
            self.state.last_direction = decision.direction
            self.state.last_candle_ts = last_ts
            self.state.cooldown_until_ts = last_ts + self.cfg.cooldown_bars * seconds_for_timeframe(self.cfg.timeframe)
            self.state.active = True
            self.state.last_signal_type = "confirmed"
            self._push_history("confirmed", ctx, last_ts)
            self._trim_history()
            self.store.save(self.state)
            return ManagerDecision("confirmed", decision.reason, True, "confirmed")

        if decision.should_prealert:
            if self.state.prealert_expiry_ts and last_ts < self.state.prealert_expiry_ts:
                return ManagerDecision("blocked", "prealert_active", False, "blocked")
            self.state.prealert_expiry_ts = last_ts + self.cfg.prealert_ttl_bars * seconds_for_timeframe(self.cfg.timeframe)
            self.state.last_signal_type = "prealert"
            self._push_history("prealert", ctx, last_ts)
            self._trim_history()
            self.store.save(self.state)
            return ManagerDecision("prealert", decision.reason, True, "prealert")

        self._push_history("blocked", ctx, last_ts)
        self._trim_history()
        self.store.save(self.state)
        return ManagerDecision("blocked", decision.reason, False, "blocked")

    def _push_history(self, state: str, ctx: str, ts: int):
        self.state.history.append({"state": state, "ctx": ctx, "ts": ts})

    def _trim_history(self):
        if len(self.state.history) > self.cfg.max_history:
            self.state.history = self.state.history[-self.cfg.max_history:]


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_message(symbol: str, decision: StrategyDecision, state: str) -> str:
    label = "PREALERTA" if state == "prealert" else "CONFIRMADA" if state == "confirmed" else state.upper()
    return (
        f"<b>{escape_html(symbol)}</b> | <b>{label}</b> | <b>{escape_html(decision.mode)}</b>
"
        f"Motivo: {escape_html(decision.reason)}
"
        f"Precio: {decision.price:.2f}
"
        f"RSI: {decision.rsi:.2f}
"
        f"Volumen: {escape_html(decision.volume_state)}
"
        f"Volatilidad: {escape_html(decision.volatility_state)}"
    )


class ProSignalApp:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.logger = BotLogger(cfg.log_level)
        self.exchange = KucoinClient(cfg.kucoin_base_url, cfg.request_timeout, cfg.request_timeout_read, cfg.request_retries)
        self.strategy = StrategyEngine()
        self.store = StateStore(cfg.state_file)
        self.manager = SignalManager(cfg, self.store)
        self.notifier = TelegramNotifier(cfg.telegram_bot_token, cfg.telegram_chat_id, cfg.telegram_parse_mode, cfg.telegram_silent)
        self.last_processed_candle_ts = 0

    def health_check(self) -> Dict[str, Any]:
        status = {"kucoin": False, "telegram": False, "candles": 0}
        try:
            candles = self.exchange.get_candles(self.cfg.symbol, self.cfg.timeframe, 5)
            status["kucoin"] = bool(candles)
            status["candles"] = len(candles)
        except Exception:
            status["kucoin"] = False
        status["telegram"] = bool(self.cfg.telegram_bot_token and self.cfg.telegram_chat_id)
        return status

    def run_once(self):
        try:
            candles = self.exchange.get_candles(self.cfg.symbol, self.cfg.timeframe, self.cfg.candles_limit)
            if not candles:
                self.logger.warning("sin datos")
                return
            if candles[-1].ts == self.last_processed_candle_ts:
                self.logger.info("misma vela, sin acción")
                return

            decision = self.strategy.evaluate(candles, self.cfg.mode, self.cfg)
            decision.context_hash = market_context_hash(candles, decision)
            managed = self.manager.evaluate(decision, candles)
            self.last_processed_candle_ts = candles[-1].ts

            self.logger.info(
                f"symbol={self.cfg.symbol} mode={self.cfg.mode} decision={decision.direction} "
                f"state={managed.state} reason={managed.reason} price={decision.price:.2f} rsi={decision.rsi:.2f}"
            )

            if managed.send_message:
                text = build_message(self.cfg.symbol, decision, managed.message_type)
                self.notifier.send(text)

        except Exception as e:
            self.logger.exception(f"error: {e}")

    def run_forever(self):
        while True:
            self.run_once()
            time.sleep(max(15, seconds_for_timeframe(self.cfg.timeframe) // 6))


def load_config_from_env() -> Config:
    return Config()


def self_test() -> bool:
    cfg = load_config_from_env()
    assert cfg.symbol == "BTC-USDT"
    assert seconds_for_timeframe("15min") == 900
    dummy_candles = [
        Candle(1, 100, 101, 102, 99, 10, 1000),
        Candle(2, 101, 103, 104, 100, 12, 1200),
        Candle(3, 103, 104, 105, 102, 15, 1500),
        Candle(4, 104, 106, 107, 103, 20, 2000),
        Candle(5, 106, 108, 109, 105, 30, 3000),
        Candle(6, 108, 110, 111, 107, 35, 3500),
        Candle(7, 110, 111, 112, 109, 40, 4000),
        Candle(8, 111, 112, 113, 110, 45, 4500),
        Candle(9, 112, 113, 114, 111, 50, 5000),
        Candle(10, 113, 114, 115, 112, 60, 6000),
        Candle(11, 114, 116, 117, 113, 70, 7000),
        Candle(12, 116, 118, 119, 115, 80, 8000),
        Candle(13, 118, 120, 121, 117, 90, 9000),
        Candle(14, 120, 123, 124, 119, 100, 10000),
        Candle(15, 123, 125, 126, 122, 110, 11000),
        Candle(16, 125, 127, 128, 124, 120, 12000),
        Candle(17, 127, 128, 129, 126, 130, 13000),
        Candle(18, 128, 130, 131, 127, 140, 14000),
        Candle(19, 130, 131, 132, 129, 150, 15000),
        Candle(20, 131, 133, 134, 130, 160, 16000),
        Candle(21, 133, 135, 136, 132, 170, 17000),
    ]
    strat = StrategyEngine()
    dec = strat.evaluate(dummy_candles, "normal", cfg)
    assert dec.direction in {"LONG", "SHORT", "NONE", "PREALERT"}
    store_path = "_test_state.json"
    try:
        store = StateStore(store_path)
        manager = SignalManager(cfg, store)
        m = manager.evaluate(dec, dummy_candles)
        assert m.state in {"confirmed", "prealert", "blocked", "cooldown"}
    finally:
        if os.path.exists(store_path):
            os.remove(store_path)
    return True


if __name__ == "__main__":
    if os.getenv("RUN_SELF_TEST", "1") == "1":
        assert self_test()
        print("SELF_TEST_OK")
    app = ProSignalApp(load_config_from_env())
    if os.getenv("RUN_FOREVER", "0") == "1":
        app.run_forever()
    else:
        app.run_once()
