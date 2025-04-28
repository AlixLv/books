from decouple import config
from sqlalchemy import create_engine, URL
from supabase import create_client, Client
from sqlalchemy.ext.declarative import declarative_base


url_db = config("SUPABASE_URL")
key_db = config("SUPABASE_KEY")
db_url_connexion = config("DB_URL")

user_db = config("user") 
password_db = config("password")
host_db = config("host")
port_db = config("port")
dbname_db = config("dbname")

url_object = URL.create("postgresql+psycopg2", username=user_db, password=password_db, host=host_db, database=dbname_db,)


# création point de départ pour intéragir avec la db, via la DBAPI
try:
    ENGINE = create_engine(db_url_connexion,  pool_pre_ping=True)
    connection = ENGINE.connect()
    print(f"Connexion SQLAlchemy réussie")
except Exception as e:
    print(f"Erreur de connexion SQLALchemy: {e}")    


Base = declarative_base()

#connexion à Supabase via son API, attention fait doublon avec ENGINE de SQLAlchemy:
def create_supabase_client():
    try:
        supabase: Client = create_client(url_db, key_db)
        print(f"🔥 successfully connected to db!")
    except ConnectionError as e:
        print(f"An error occured while trying to connect to db: {e}")
            
    return supabase