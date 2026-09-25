import os

from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/manage/health")
def health():
    print(os.environ.get("FLIGHT_SERVICE_DB", ""))
    return {"status": "healthy"}