from datetime import date
from typing import List
from fastapi.testclient import TestClient
from src.constants import holyday_list
from src.main import app
from pydantic import TypeAdapter

test_client = TestClient(app)

def test_holidays():
    response = test_client.get("/holidays")
    holyday_list_adapter = TypeAdapter(List[date])
    assert response.status_code == 200
    assert holyday_list_adapter.validate_python(response.json()) == holyday_list
    #Note: data might change criteria is it following the schema and being valid.
