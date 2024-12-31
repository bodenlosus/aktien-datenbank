import sys
import time

from .database.depots import updateDepotValues
from .download import download
from dotenv import dotenv_values
from supabase import Client
import yfinance as yf
import pathlib
from .database.insert_prices import uploader
from .database.stock_info import getStockInfo
from .database.client import createSupabaseClient
from .track_records import TrackRecord
import queue
import threading


def getStocks(stockInfos) -> dict[str, int]:
    stocks = {symbol.upper():id for id, symbol in stockInfos}
    return stocks

def update():
    url, key = getSecrets()
    
    supabase: Client = createSupabaseClient(timeout=30, url=url, key=key)
    
    updateStocks(supabase)
    updateDepots(supabase)
    
def updateDepots(supabase):
    dRecord_file = pathlib.Path("./depot_record.dat")
    dRecord_file.touch(exist_ok=True)
    
    dRecord = TrackRecord(dRecord_file)
    dRecord.readRecord()
    start = dRecord.getLastUpdateDate(0)
    end = dRecord.getCurrentDate()
    
    updateDepotValues(
        supabase, 
        start=dRecord.toTimestamp(start), 
        end=dRecord.toTimestamp(end),
    )
    
    dRecord.updateRecord([0,])
    
    dRecord.saveRecord()

def updateStocks(supabase):
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
        
        lastUpdate = record.getLastUpdateDate(id)

        dataframe, lastUpdateTS = download(
            symbol=symbol, 
            id=id, 
            start=record.toTimestamp(lastUpdate)
            )
        
        time.sleep(0.1)
        if dataframe.empty:
            continue
        
        q.put((dataframe, dataframe.shape[0]))
        
        record.updateRecord([id,], record.parseTimestamp(lastUpdateTS))
    
    record.saveRecord()
    
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