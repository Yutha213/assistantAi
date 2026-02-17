import os
from supabase import create_client, Client
from dotenv import load_dotenv

def check_dimensions():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url or not key:
        print("Error: Supabase credentials not found in .env")
        return

    try:
        supabase: Client = create_client(url, key)
        # Fetch one record to inspect the embedding dimension
        response = supabase.table("knowledge_base").select("embedding").limit(1).execute()
        
        if not response.data:
            print("No data found in knowledge_base table. Please insert at least one record or specify the dimension.")
            return

        embedding = response.data[0].get("embedding")
        if embedding:
            # The embedding is returned as a string like "[0.1, 0.2, ...]" or a list
            if isinstance(embedding, str):
                import json
                try:
                    embedding = json.loads(embedding)
                except:
                    # Strip brackets and split
                    embedding = embedding.strip("[]").split(",")
            
            dimension = len(embedding)
            print(f"Detected Dimension: {dimension}")
            
            if dimension == 768:
                print("Likely Model: Jina v2 or Google text-embedding-004")
            elif dimension == 1024:
                print("Likely Model: Jina v3 (Default), Mosaic, or OpenAI v3-small (Default)")
            elif dimension == 1536:
                print("Likely Model: OpenAI ada-002 or v3-small (Custom)")
            elif dimension == 2048:
                print("Likely Model: Jina v4")
            else:
                print(f"Unknown model for dimension {dimension}")
        else:
            print("Embedding column exists but the first row is empty.")

    except Exception as e:
        print(f"Error connecting to Supabase: {e}")

if __name__ == "__main__":
    check_dimensions()
