
import pandas as pd


def add_indicators(df):
    df = df.copy()

    # Simple moving averages
    df["SMA_7"] = df["close"].rolling(window=7).mean()
    df["SMA_25"] = df["close"].rolling(window=25).mean()

    # RSI (14 periods)
    delta = df["close"].diff()

    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    avg_gain = gains.rolling(window=14).mean()
    avg_loss = losses.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))

    return df
