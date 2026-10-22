
from tools.btc_analysis import get_btc_analysis

analysis = get_btc_analysis()

for key, value in analysis.items():
    print(f"{key}: {value}")
