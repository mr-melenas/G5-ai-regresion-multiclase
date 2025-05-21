import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def save(data_dict):
    try:
        response = supabase.table("forrest").insert(data_dict).execute()
        print("Fila guardada correctamente en la base de datos (supabase).")
        return response
    except Exception as e:
        print("Error al guardar en Supabase:", e)
        return None

def save_data(features, prediction):
    try:
        data_dict = {
            "created_at": datetime.now().isoformat(),
            "features": features,
            "label": prediction     
        }
        print("data_dict:", data_dict)
        save(data_dict)
    except Exception as e:
        print("BD Error while saving data:", e)

        return None