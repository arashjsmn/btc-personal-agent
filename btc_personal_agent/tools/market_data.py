
import requests
import pandas as pd


def get_btc_market_data(limit=100):
    url = "https://data-api.binance.vision/api/v3/klines"

    params = {
        "symbol": "BTCUSDT",
        "interval": "1d",
        "limit": limit
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()
    data = response.json()

    columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_volume",
        "trades",
        "taker_buy_volume",
        "taker_buy_quote_volume",
        "ignore"
    ]

    df = pd.DataFrame(data, columns=columns)

    df["date"] = pd.to_datetime(
        df["open_time"],
        unit="ms",
        utc=True
    )

    numeric_columns = [
        "open", "high", "low",
        "close", "volume"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column])

    return df
