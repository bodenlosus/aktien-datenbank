import numpy as np
from utils.np_to_native import npDTypeToNative


def parsePriceFrame(el, stockID):
    el.reset_index()
    c = 0
    for index, row in el.iterrows():
        price = {
            "stock_id": np.int64(stockID),
            "timestamp": index.strftime("%Y-%m-%d"),
            "open": round(row["Open"], 4),
            "close": round(row["Close"], 4),
            "high": round(row["High"], 4),
            "low": round(row["Low"], 4),
            "volume": row["Volume"].astype(np.int64),
        }
        
        if True in [np.isnan(price[i]) for i in ["open", "close", "high", "low"]]:
            print(f"Missing data for {stockID} on {index.strftime('%Y-%m-%d')}")
            continue
        
        c += 1
        
        yield {key: npDTypeToNative(value)[0] for key, value in price.items()}