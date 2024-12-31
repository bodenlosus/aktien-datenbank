from typing import Tuple
from pandas import DataFrame
import yfinance as yf

def download(symbol, id, start:str=None, end:str=None, period="1y") ->Tuple[DataFrame, str]:
    ticker = yf.Ticker(symbol)
    dataframe = (ticker.history(period=period, start=start, end=end)
                 .dropna()
                 .reset_index()
                 )
    
    if dataframe.empty:
        print(f"No data found: period={period}, Stock={symbol} with ID={id}")
        return dataframe, None
    
    columnsToKeep = ["Date", "Ticker", "Close", "High", "Low", "Open", "Volume"]
    
    columnsToDrop = [column for column in dataframe.columns if column not in columnsToKeep] 
    
    dataframe.drop(columns=columnsToDrop, errors="ignore", inplace=True)
    dataframe.columns = ["timestamp", "close", "high", "low", "open", "volume"]
    
    dataframe["stock_id"] = id
    dataframe["timestamp"] = dataframe["timestamp"].apply(lambda dt: dt.strftime("%Y-%m-%d"))
    dataframe = dataframe.astype({"volume":"int"})
    lastValue = dataframe["timestamp"].iloc[-1]
    return dataframe, lastValue