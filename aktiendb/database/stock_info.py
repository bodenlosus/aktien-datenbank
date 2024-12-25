from collections.abc import Generator
from supabase import Client


def getStockInfo(supabase: Client, keys: tuple[str]) -> Generator[str, None, None]:

    chunk_number = 0
    chunk_size = 500

    while True:
        try:
            response = supabase.rpc(
                "paginate_stock_symbols",
                {"chunk_size": chunk_size, "chunk_number": chunk_number},
            ).execute()

        except Exception as e:
            print(f"Failed to fetch stock info: {e}")
            raise e

        for row in response.data:
            yield (row[key] for key in keys)

        chunk_number += 1

        if len(response.data) < chunk_size:
            break