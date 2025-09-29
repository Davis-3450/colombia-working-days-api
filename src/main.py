from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import PositiveInt
from src.logic import Calculator


# error: { "error": "InvalidParameters", "message": "Detalle del error" }

app = FastAPI()


# TODO: make custom fields
@app.get("/calculate")
def calculate(days: PositiveInt = None, hours: PositiveInt = None, date: datetime = None):
    calculator = Calculator(days=days, hours=hours, date=date)
    r = calculator.calculate()
    return Response(date=r)

# get holidays | not a requirement
@app.get("/holidays")
def get_holidays():
    return holyday_list



