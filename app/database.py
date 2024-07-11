from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .config import settings


try:
    conn = psycopg2.connect(host='localhost', database='myfastapi', user='postgres', 
                            password='password123', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('successfull connection to Database')
except Exception as e:
    print("failed to connect to Database")
    print("error: ", e)



# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/myfastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()