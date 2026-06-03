import os
import json
import requests
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

STATE_FILE = "paper_trades.json"


def send(msg):
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=20
    )

    print("Telegram:", r.status_code)


def load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


try:

    state = load_state()

    r = requests.get(
        "https://api.coingecko.com/api/v3/coins/ethereum/market_chart",
        params={
            "vs_currency": "usd",
            "days": "7",
            "interval": "hourly"
        },
        timeout=20
    )

    data = r.json()

    if "prices" not in data:
        raise Exception("Price data not found")

    prices = [x[1] for x in data["prices"]]

    df = pd.DataFrame()
    df["close"] = prices

    ema21 = EMAIndicator(df["close"], window=21).ema_indicator()
    ema50 = EMAIndicator(df["close"], window=50).ema_indicator()
    rsi = RSIIndicator(df["close"], window=14).rsi()

    price = float(df["close"].iloc[-1])
    ema21_now = float(ema21.iloc[-1])
    ema50_now = float(ema50.iloc[-1])
    rsi_now = float(rsi.iloc[-1])

    print("Price:", round(price, 2))
    print("EMA21:", round(ema21_now, 2))
    print("EMA50:", round(ema50_now, 2))
    print("RSI:", round(rsi_now, 2))

    trade = state["open_trade"]

    # CHECK EXISTING TRADE
    if trade is not None:

        if price >= trade["tp"]:

            profit = state["balance"] * 0.02

            state["balance"] += profit
            state["wins"] += 1
            state["open_trade"] = None

            save_state(state)

            send(
                f"""🎯 TAKE PROFIT HIT

Entry: {trade['entry']}
Exit: {price:.2f}

Profit: ${profit:.2f}

Balance: ${state['balance']:.2f}
"""
            )

            print("TP HIT")
            exit()

        elif price <= trade["sl"]:

            loss = state["balance"] * 0.01

            state["balance"] -= loss
            state["losses"] += 1
            state["open_trade"] = None

            save_state(state)

            send(
                f"""🛑 STOP LOSS HIT

Entry: {trade['entry']}
Exit: {price:.2f}

Loss: ${loss:.2f}

Balance: ${state['balance']:.2f}
"""
            )

            print("SL HIT")
            exit()

    score = 0

    if price > ema21_now:
        score += 30

    if ema21_now > ema50_now:
        score += 40

    if rsi_now > 50:
        score += 30

    print("Score:", score)

    # OPEN NEW TRADE
    if score >= 60 and state["open_trade"] is None:

        stop_loss = round(price * 0.99, 2)
        take_profit = round(price * 1.02, 2)

        state["open_trade"] = {
            "entry": price,
            "sl": stop_loss,
            "tp": take_profit
        }

        state["total_trades"] += 1

        save_state(state)

        send(
            f"""🟢 PAPER TRADE OPENED

Price: ${price:.2f}

EMA21: {ema21_now:.2f}
EMA50: {ema50_now:.2f}
RSI: {rsi_now:.2f}

Confidence: {score}/100

SL: ${stop_loss}
TP: ${take_profit}

Balance: ${state['balance']:.2f}

Mode: PAPER
"""
        )

        print("TRADE OPENED")

    else:
        print("No setup found")

except Exception as e:
    print("ERROR:", str(e))
