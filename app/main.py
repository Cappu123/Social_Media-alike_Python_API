"""importing necessary libraries and modules"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, authentication, vote
from pydantic_settings import BaseSettings
from .config import settings


print(settings.database_username)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
"""creates an app instance"""

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)

@app.get("/")
def root():
    """starts the app"""
    return {"message": "Welcome to your API"}


