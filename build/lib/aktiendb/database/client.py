from supabase import Client, create_client
from supabase.client import ClientOptions


def createSupabaseClient(timeout: int, url: str, key: str) -> Client:

    print("Connecting to Supabase...")

    try:
        client: Client = create_client(
            url,
            key,
            options=ClientOptions(
                postgrest_client_timeout=timeout,
                storage_client_timeout=timeout,
                schema="public",
            ),
        )
    except Exception as e:
        print(f"Failed to connect to Supabase: {e}")
        raise e

    print("Supabase client created successfully!")

    return client