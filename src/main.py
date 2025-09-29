from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import PositiveInt
from constants import holyday_list

# error: { "error": "InvalidParameters", "message": "Detalle del error" }

app = FastAPI()


# TODO: make custom fields
@app.get("/calculate")
def calculate(days: PositiveInt = None, hours: PositiveInt = None, date: datetime = None):
def name(days: int = None, hours: int = None, date: datetime = None):
    return "InvalidResponse()"


# get holidays | not a requirement
@app.get("/holidays")
def get_holidays():
    return holyday_list



