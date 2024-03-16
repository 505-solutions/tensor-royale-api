import os

import dotenv
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

dotenv.load_dotenv()

# Dummy wait for db to connect
while True:
    try:
        conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )
        print("Connected to database")
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

engine = create_engine(database_uri)
SessionMaker = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = SessionMaker.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
