from fastapi.testclient import TestClient
from app.main import app
from app import schemas, models
from app.database import get_db, Base
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/myfastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
"""setting the TestClient class to a variable
called client"""

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert (res.json().get('message')) == "Welcome to your API"
    assert res.status_code == 200
def test_create_user():
    res = client.post("/users", json={"email": "cappyeee@gmail.com", "password": "cappy123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "cappyeee@gmail.com"
    assert res.status_code == 201