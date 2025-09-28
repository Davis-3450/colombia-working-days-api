from datetime import datetime
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
HOLIDAYS = os.getenv("HOLYDAYS")

# get days on cold boot (why anything else lol?)

# error: { "error": "InvalidParameters", "message": "Detalle del error" }

# Note we could use a cron job to update the holidays, calculating on each request is stupid, for now lets do it on cold boot
with httpx.Client() as client:
    r = client.get(HOLIDAYS)
    working_days = r.json()


app = FastAPI()


# TODO: make custom fields
@app.get("/calculate")
def name(days: int = None, hours: int = None, date: datetime = None):
    return "InvalidResponse()"


# end def
