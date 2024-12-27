import os
import sys
from .download import downloadStocks
from dotenv import dotenv_values
from supabase import Client
import yfinance as yf
import math
import numpy as np
import pathlib
from .database.insert_prices import bulkInsertPrice, uploader
from .database.stock_info import getStockInfo
from .database.client import createSupabaseClient
from .stocks.parse_price_frame import parsePriceFrame
from .track_records import TrackRecord
import queue
import threading
import time

from itertools import batched

def getStocks(stockInfos) -> dict[str, int]:
    stocks = {symbol.upper():id for id, symbol in stockInfos}
    return stocks

def update():
    url, key = getSecrets()
    
    supabase: Client = createSupabaseClient(timeout=30, url=url, key=key)
    
    stockInfos = getStockInfo(supabase, keys=("id", "symbol"))
    
    q = queue.Queue()
    
    worker = threading.Thread(target=uploader, args=(q, supabase, 1500))
    worker.start()
    
    record_file = pathlib.Path("./record.dat")
    record_file.touch(exist_ok=True)
    
    record = TrackRecord(record_file)
    record.readRecord()
    
    for id, symbol in stockInfos:
        print("Downloading stock data for", symbol, id, sep=" ")
        
        period = record.getUpdatePeriod(id)

        dataframe = downloadStocks(symbol=symbol, id=id, period=period)
        if dataframe.empty:
            continue
        
        q.put((dataframe, dataframe.shape[0]))
    
    q.put((None, None))
    
    worker.join()

def getSecrets():
    config = dotenv_values(".env")
    url = config.get("SUPABASE_URL")
    key = config.get("SUPABASE_SERVICE_KEY")
    
    if not url:
        url = sys.argv[1]
    if not key:
        key = sys.argv[2]

    return(url, key)

if __name__ == "__main__":
    update()