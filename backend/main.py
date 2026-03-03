from database import engine
from models import Base
from fastapi import FastAPI

#Base.metadata.create_all(bind=engine)
app=FastAPI()

@app.get("/")
def greet():
    return("Backend :D")