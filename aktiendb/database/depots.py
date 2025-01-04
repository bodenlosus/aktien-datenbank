import postgrest
from supabase import Client

def updateDepotValues(supabase: Client, start:str, end:str) -> None:
    try:
        supabase.rpc("batch_update_depot_values", {"start_date":start, "end_date":end}).execute()
    except Exception as e:
        print(f"Failed to update depot values: {e}")
    except postgrest.exceptions.APIError as e:
        print(f"Failed to update depot values: {e}")
    
    print(f"Updated depot values for {start} till {end}")