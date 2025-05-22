import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv() 

url_db = os.getenv("SUPABASE_URL")
key_db = os.getenv("SUPABASE_KEY")
db_url_connexion = os.getenv("DB_URL")

user=os.getenv('user')
password=os.getenv('password')
host=os.getenv('host')
port=os.getenv('port')
dbname=os.getenv('dbname')


URL_CONNEXION = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"


# création point de départ pour intéragir avec la db, via la DBAPI
try:
    ENGINE = create_engine(URL_CONNEXION, pool_pre_ping=True, echo=True)
    connection = ENGINE.connect()
    print(f"Connexion SQLAlchemy réussie")
except Exception as e:
    print(f"Erreur de connexion SQLALchemy: {e}")    


# session = création de l'interface pour intéragir avec la db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

Base = declarative_base()


def get_session():
    """Créer une session pour les opérations sur la base."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()





