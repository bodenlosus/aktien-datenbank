from alpha_vantage.timeseries import TimeSeries
from pandas import DataFrame

def download(symbol, id, oldest:str) -> DataFrame:
    """
    Download historical stock data from Alpha Vantage for a given symbol and ID.
    Prepares it for database insertion.

    Parameters:
    symbol (str): The stock symbol to download data for.
    id (int): The unique to assign to the stock.
    oldest (str): The oldest date (YYYY-MM-DD) for which data will be included.

    Returns:
    DataFrame: A pandas DataFrame containing the historical stock data with the following columns:
        - timestamp: The date of the stock data.
        - open: The opening price of the stock.
        - high: The highest price of the stock.
        - close: The closing price of the stock.
        - low: The lowest price of the stock.
        - volume: The volume of the stock.
        - stock_id: The unique identifier for the stock.
    """
    ts = TimeSeries(key="WBWQASL71SX0NAZ7", output_format="pandas")
    dataframe: DataFrame
    dataframe, meta_data = ts.get_daily(symbol="msft", outputsize="compact")

    if dataframe.empty:
        print(f"No data found: Stock={symbol} with ID={id}")
        return dataframe

    dataframe.dropna(inplace=True)

    # Find the column and drop earlier ones
    dataframe = dataframe.loc[oldest:]

    dataframe.reset_index(inplace=True)

    dataframe.columns = ["timestamp", "open", "high", "close", "low", "volume"]
    dataframe["stock_id"] = id
    dataframe = dataframe.astype({"volume":"int"})

    lastValue = dataframe["timestamp"][0]
    return dataframe

# def downloadToday(symbols, id):
#     ts = TimeSeries(key="WBWQASL71SX0NAZ7", output_format="pandas", indexing_type="integer")
#     dataframe: DataFrame
#     dataframe, meta_data = ts.get_quote_endpoint(symbol="msft")
    
#     if dataframe.empty:
#         print(f"No data found: Stock={symbols} with ID={id}")
#         return dataframe
    
#     dataframe.dropna(inplace=True)
#     dataframe.columns = ["timestamp", "open", "high", "close", "low", "volume"]

#     dataframe["stock_id"] = id
#     dataframe = dataframe.astype({"volume":"int"})

if __name__ == "__main__":
    print(download("msft", 13, "2024-12-12"))