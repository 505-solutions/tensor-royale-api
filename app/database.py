import os

import dotenv
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

dotenv.load_dotenv()

# Dummy wait for db to connect
while True:
    try:
        conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            port=os.environ['POSTGRES_PORT'],
            password=os.environ['POSTGRES_PASSWORD'],
        )
        print("Connected to database")

        all_tables = "select table_name from information_schema.tables WHERE table_schema = 'public' AND table_name NOT LIKE '%alembic%'"
        cursor = conn.cursor()
        cursor.execute(all_tables)
        tables = cursor.fetchall()
        # drop all tables
        print(tables)
        for table in tables:
            cursor.execute(f"DROP TABLE \"{table[0]}\" CASCADE")
        conn.commit()
        cursor.close()
        conn.close()
        print("Setup Tables")
        break
    except Exception as e:
        print(os.environ['POSTGRES_HOST'])
        print("Exception custom:", e)
        continue

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['POSTGRES_USER'],
    dbpass=os.environ['POSTGRES_PASSWORD'],
    dbhost=os.environ['POSTGRES_HOST'],
    dbname=os.environ['POSTGRES_DB']
)

engine = create_engine(database_uri, pool_size=10, max_overflow=20)
SessionMaker = sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine)
Base = declarative_base()
# Base.query = SessionMaker.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
