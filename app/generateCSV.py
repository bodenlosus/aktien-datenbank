from io import TextIOWrapper
from dotenv import dotenv_values
from supabase import Client
import yfinance as yf
import numpy as np
import pathlib
from app.database.insert_prices import bulkInsertPrice
from app.database.stock_info import getStockInfo
from app.database.client import createSupabaseClient
from app.stocks.parse_price_frame import parsePriceFrame
from app.track_records import TrackRecord
# main
def update():
    config = dotenv_values(".env")
    
    supabase: Client = createSupabaseClient(timeout=30, url=config["SUPABASE_URL"], key=config["SUPABASE_SERVICE_KEY"])
    
    stockInfos = getStockInfo(supabase, keys=("id", "symbol"))
    
    record_file = pathlib.Path("./record_csvup.dat")
    record_file.touch(exist_ok=True)
    
    record = TrackRecord(record_file)
    record.readRecord()
    
    price_file = pathlib.Path("./prices.csv")
    price_file.touch(exist_ok=True)
    f = open(price_file, "a")
    f.write("stock_id;timestamp;open;close;high;low;volume\n")

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
        parseToCSV(f,parsePriceFrame(el, id))
            
        record.updateRecord([id,])
    f.close()
def parseToCSV(f:TextIOWrapper, prices:list[dict[str, float]],):
    for price in prices:
        line = ""
        for i in price.values():
            line += f"{i};"
        f.write(line.strip(";") + "\n")
if __name__ == "__main__":
    update()