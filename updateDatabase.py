from dotenv import dotenv_values
from supabase import Client
import yfinance as yf
import math
import numpy as np

from database.insert_prices import bulkInsertPrice
from database.stock_info import getStockInfo
from database.client import createSupabaseClient
from stocks.parse_price_frame import parsePriceFrame
from track_records import TrackRecord
# main
if __name__ == "__main__":
    config = dotenv_values(".env")
    
    supabase: Client = createSupabaseClient(timeout=30, url=config["SUPABASE_URL"], key=config["SUPABASE_SERVICE_KEY"])
    
    stockInfos = getStockInfo(supabase, keys=("id", "symbol"))
    
    record = TrackRecord("./record.dat")
    record.readRecord()

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
        
        # DataFrame-Werte in normale arrays schreiben
        response = bulkInsertPrice(supabase, parsePriceFrame(el, id), chunk_size=500)
        
        if isinstance(response, Exception):
            print(f"Error inserting data for {symbol}: {response}")
            continue
        
        record.updateRecord([id,])