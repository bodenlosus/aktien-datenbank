import os
import sys
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

def update():
    config = dotenv_values(".env")
    url = config.get("SUPABASE_URL")
    key = config.get("SUPABASE_SERVICE_KEY")
    
    if not url:
        url = sys.argv[1]
    if not key:
        key = sys.argv[2]

    print(url, key)
    
    supabase: Client = createSupabaseClient(timeout=30, url=url, key=key)
    
    stockInfos = getStockInfo(supabase, keys=("id", "symbol"))
    
    record_file = pathlib.Path("./record.dat")
    record_file.touch(exist_ok=True)
    
    record = TrackRecord(record_file)
    record.readRecord()

    q = queue.Queue()
    
    worker = threading.Thread(target=uploader, args=(q, supabase, 600))
    worker.start()
    
    for id, symbol in stockInfos:
        print(f"Aktie {id}: {symbol}")
        # Stellt panda-Dataframe mit den relevanten Werten zur Verfügung
       
        try:
            msft = yf.Ticker(symbol)
            el = msft.history(period=record.getUpdatePeriod(id))
        except ValueError:
            print("Keine Daten vorhanden für ", symbol)
            continue
        except Exception as e:
            print(f"Fehler beim Abrufen von Daten für {symbol}: {e}")
            continue
        
        count = len(el)
        prices = parsePriceFrame(el, id)
        
        q.put((prices, count))
        
        record.updateRecord([id,])
    
    q.put((None, None))
    
    worker.join()
        
if __name__ == "__main__":
    update()