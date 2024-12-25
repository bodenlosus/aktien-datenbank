import sys
import time
import postgrest
from supabase import Client


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
        
        

