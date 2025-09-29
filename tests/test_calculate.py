from fastapi.testclient import TestClient

from src.main import app

test_client = TestClient(app)


# 1. Petición un viernes a las 5:00 p.m. con "hours=1"
#    Resultado esperado: lunes a las 9:00 a.m. (hora Colombia) → "2025-XX-XXT14:00:00Z" (UTC)
def test_1():
    response = test_client.get("/calculate?hours=1")
    assert response.status_code == 200
    assert response.json() == {"date": "2025-08-01T14:00:00Z"}


# 2. Petición un sábado a las 2:00 p.m. con "hours=1"
#    Resultado esperado: lunes a las 9:00 a.m. (hora Colombia) → "2025-XX-XXT14:00:00Z" (UTC)
def test_2():
    response = test_client.get("/calculate?hours=1")
    assert response.status_code == 200
    assert response.json() == {"date": "2025-08-01T14:00:00Z"}


# 3. Petición con "days=1" y "hours=4" desde un martes a las 3:00 p.m.
#    Resultado esperado: jueves a las 10:00 a.m. (hora Colombia) → "2025-XX-XXT15:00:00Z" (UTC)
def test_3():
    response = test_client.get("/calculate?days=1&hours=4")
    assert response.status_code == 200
    assert response.json() == {"date": "2025-08-01T15:00:00Z"}


# 4. Petición con "days=1" desde un domingo a las 6:00 p.m.
#    Resultado esperado: lunes a las 5:00 p.m. (hora Colombia) → "2025-XX-XXT22:00:00Z" (UTC)
def test_4():
    response = test_client.get("/calculate?days=1")
    assert response.status_code == 200
    assert response.json() == {"date": "2025-08-01T22:00:00Z"}


# 5. Petición con "hours=8" desde un día laboral a las 8:00 a.m.
#    Resultado esperado: mismo día a las 5:00 p.m. (hora Colombia) → "2025-XX-XXT22:00:00Z" (UTC)
def test_5():
    response = test_client.get("/calculate?hours=8")
    assert response.status_code == 200
    assert response.json() == {"date": "2025-08-01T22:00:00Z"}


# 6. Petición con "days=1" desde un día laboral a las 8:00 a.m.
#    Resultado esperado: siguiente día laboral a las 8:00 a.m. (hora Colombia) → "2025-XX-XXT13:00:00Z" (UTC)
def test_6():
    response = test_client.get("/calculate?days=1")
    assert response.status_code == 200
    assert response.json() == {"date": "2025-08-01T13:00:00Z"}


# 7. Petición con "days=1" desde un día laboral a las 12:30 p.m.
#    Resultado esperado: siguiente día laboral a las 12:00 p.m. (hora Colombia) → "2025-XX-XXT17:00:00Z" (UTC)
def test_7():
    response = test_client.get("/calculate?days=1")
    assert response.status_code == 200
    assert response.json() == {"date": "2025-08-01T17:00:00Z"}


# 8. Petición con "hours=3" desde un día laboral a las 11:30 p.m.
#    Resultado esperado: mismo día laboral a las 3:30 p.m. (hora Colombia) → 2025-XX-XXT20:30:00Z (UTC)
def test_8():
    response = test_client.get("/calculate?hours=3")
    assert response.status_code == 200
    assert response.json() == {"date": "2025-08-01T20:30:00Z"}


# 9. Petición con "date=2025-04-10T15:00:00.000Z" y "days=5" y "hours=4" (el 17 y 18 de abril son festivos)
#    Resultado esperado: 21 de abril a las 3:30 p.m. (hora Colombia) → "2025-04-21T20:00:00.000Z" (UTC)
def test_9():
    response = test_client.get(
        "/calculate?date=2025-04-10T15:00:00.000Z&days=5&hours=4"
    )
    assert response.status_code == 200
    assert response.json() == {"date": "2025-04-21T20:00:00.000Z"}


# errors

def test_error_1():
    """
    No parameters
    """
    response = test_client.get("/calculate")
    assert response.status_code == 400
    # assert response.json() == {"error": "InvalidParameters", "message": "Invalid parameters"}

def test_error_2():
    """
    Invalid parameters (invalid date)
    """
    response = test_client.get("/calculate?days=1&hours=1&date=2025-08-01T15:00:00.000Z")