from tools.market_data import get_btc_market_data

df = get_btc_market_data()

print(df[["date", "close", "volume"]].tail())
print("\nNumber of candles:", len(df))
print("\nLatest observed close:", df["close"].iloc[-1])