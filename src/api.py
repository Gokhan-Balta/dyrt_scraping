# api.py
from fastapi import FastAPI
from scheduler import start_scheduler

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await start_scheduler()

@app.get("/")
def root():
    return {"message": "API is working"}
