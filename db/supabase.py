from decouple import config
from sqlalchemy import create_engine
from supabase import create_client, Client


url_db = config("SUPABASE_URL")
key_db = config("SUPABASE_KEY")
db_url_connexion = config("DB_URL")

# création point de départ pour intéragir avec la db, via la DBAPI
ENGINE = create_engine(db_url_connexion)
connection = ENGINE.connect()

#connexion à Supabase:
def create_supabase_client():
    try:
        supabase: Client = create_client(url_db, key_db)
        print(f"🔥 successfully connected to db!")
    except ConnectionError as e:
        print(f"An error occured while trying to connect to db: {e}")
            
    return supabase