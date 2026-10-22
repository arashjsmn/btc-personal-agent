
from tools.market_data import get_btc_market_data
from tools.indicators import add_indicators

df = get_btc_market_data()
df = add_indicators(df)

print(
    df[["date", "close", "SMA_7", "SMA_25", "RSI_14"]].tail(10)
)

latest = df.iloc[-1]

print("\n--- Latest Indicators ---")
print("Close:", latest["close"])
print("SMA 7:", latest["SMA_7"])
print("SMA 25:", latest["SMA_25"])
print("RSI 14:", latest["RSI_14"])
