
from tools.market_data import get_btc_market_data
from tools.indicators import add_indicators


def get_btc_analysis():
    # 1. Get market data
    df = get_btc_market_data(limit=100)

    # 2. Calculate indicators
    df = add_indicators(df)

    # 3. Select the latest candle
    latest = df.iloc[-1]

    # 4. Prepare a simple trend description
    if latest["SMA_7"] > latest["SMA_25"]:
        trend = "short-term average above long-term average"
    else:
        trend = "short-term average below long-term average"

    # 5. Return the information
    return {
        "date": latest["date"].isoformat(),
        "close": float(latest["close"]),
        "volume": float(latest["volume"]),
        "sma_7": float(latest["SMA_7"]),
        "sma_25": float(latest["SMA_25"]),
        "rsi_14": float(latest["RSI_14"]),
        "trend": trend
    }
