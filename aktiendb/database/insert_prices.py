from itertools import batched, chain
import sys
import time
from typing import Generator
import postgrest
from supabase import Client
import queue
import threading

def uploader(q: queue.Queue, supabase: Client, chunKSize=500):
    prices = []
    priceCount = 0
    while True:
        frame, amount = q.get()
        
        if frame is None:
            break
        
        priceCount += amount
        
        prices.extend(frame.to_dict(orient="records"))

        if priceCount >= chunKSize:
            response = bulkInsertPrice(supabase, prices, chunk_size=chunKSize)
            
            if isinstance(response, Exception):
                print(f"Error inserting data")
            
            prices = []
            priceCount = 0
            
    if priceCount > 0:
        response = bulkInsertPrice(supabase, prices, chunk_size=500)
            
        if isinstance(response, Exception):
            print(f"Error inserting data")
    
    q.task_done()
    
            
            
        

def bulkInsertPrice(
    supabase: Client,
    prices: list[dict[str, str | float | int]],
    chunk_size: int = 500,
):
    # Bulk in chunks
    for bulk in batched(prices, chunk_size): 
        try:
            response = supabase.rpc(
                "upsert_stock_prices_bulk",
                {"p_data": bulk},
            ).execute()
        except postgrest.exceptions.APIError as e:
            print(*bulk, sep="\n", file=sys.stderr)
            raise(e)
        except Exception as e:
            print(f"Failed to insert data: {e}")
        print(f"Inserted {len(bulk)} rows.")
        time.sleep(.5)
    print("inserted.")
        

