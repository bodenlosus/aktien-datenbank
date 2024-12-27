from pandas import DataFrame
import yfinance as yf

def getID(stocks, symbol:str ) -> int:
    id = stocks.get(symbol.upper(), -1)
    
    if id == -1:
        print(stocks)
        print(symbol)
        raise ValueError(f"No stock found for {symbol}")

    return id
def downloadStocks(symbol, id, start:str=None, end:str=None, period="1y") -> DataFrame:
    ticker = yf.Ticker(symbol)
    dataframe = (ticker.history(period=period, start=start, end=end)
                 .dropna()
                 .reset_index()
                 )
    
    if dataframe.empty:
        print("No data found for the given period")
        return dataframe
    
    columnsToKeep = ["Date", "Ticker", "Close", "High", "Low", "Open", "Volume"]
    
    columnsToDrop = [column for column in dataframe.columns if column not in columnsToKeep] 
    
    dataframe.drop(columns=columnsToDrop, errors="ignore", inplace=True)
    dataframe.columns = ["timestamp", "close", "high", "low", "open", "volume"]
    
    dataframe["stock_id"] = id
    dataframe["timestamp"] = dataframe["timestamp"].apply(lambda dt: dt.strftime("%Y-%m-%d"))
    dataframe = dataframe.astype({"volume":"int"})
    return dataframe