from itertools import chain
import sys
import time
from typing import Generator
import postgrest
from supabase import Client
import queue
import threading

def uploader(q: queue.Queue, supabase: Client, chunKSize=500):
    pricesGens = []
    priceCount = 0
    while True:
        gen, amount = q.get()
        
        if gen is None:
            break
        
        priceCount += amount
        
        pricesGens.append(gen)

        if priceCount >= chunKSize:
            priceChain = chain(*pricesGens[:])
            response = bulkInsertPrice(supabase, priceChain, chunk_size=chunKSize)
            
            if isinstance(response, Exception):
                print(f"Error inserting data")
            
            pricesGens = []
            priceCount = 0
            
    if priceCount > chunKSize:
        priceChain = chain(*pricesGens[:])
        response = bulkInsertPrice(supabase, priceChain, chunk_size=500)
            
        if isinstance(response, Exception):
            print(f"Error inserting data")
    
    q.task_done()
    
            
            
        

def bulkInsertPrice(
    supabase: Client,
    prices: list[dict[str, str | float | int]],
    chunk_size: int = 500,
):
    inserted_count = 0

    price = next(prices, None)
    # Bulk in chunks
    while price is not None:
        bulk = []
        for i in range(chunk_size):

            bulk.append(price)
            price = next(prices, None)
            inserted_count += 1
            if price is None:
                break
        
        try:
            response = supabase.rpc(
                "upsert_stock_prices_bulk",
                {"p_data": bulk},
            ).execute()
        except postgrest.exceptions.APIError as e:
            print(*bulk, sep="\n", file=sys.stderr)
        except Exception as e:
            print(f"Failed to insert data: {e}")
        print(f"Inserted {inserted_count} rows.")
        time.sleep(.5)
    print("inserted.")
        

