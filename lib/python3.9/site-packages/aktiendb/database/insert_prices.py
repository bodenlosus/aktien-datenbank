import sys
import time
from typing import Dict, Generator, List, Union
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
            
            prices = []
            priceCount = 0
            
            if isinstance(response, Exception):
                print(f"Error inserting data")
            
    if priceCount > 0:
        response = bulkInsertPrice(supabase, prices, chunk_size=500)
            
        if isinstance(response, Exception):
            print(f"Error inserting data")
    
    q.task_done()
    
            
            
        

def bulkInsertPrice(
    supabase: Client,
    prices: List[Dict[str, Union[str , float , int]]],
    chunk_size: int = 500,
):
    # Bulk in chunks
    for i in range(0, len(prices), chunk_size):
        endi = i + (chunk_size)
        bulk = prices[i:endi]
        try:
            response = supabase.rpc(
                "upsert_stock_prices_bulk",
                {"p_data": bulk},
            ).execute()
        except postgrest.exceptions.APIError as e:
            print(*bulk, sep="\n", file=sys.stderr)
        except Exception as e:
            print(f"Failed to insert data: {e}")
        print(f"Inserted {len(bulk)} rows.")
        time.sleep(.5)
    print("inserted.")
        

