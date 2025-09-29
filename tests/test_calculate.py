from fastapi.testclient import TestClient

from src.main import app

test_client = TestClient(app)
C = "/calculate"

# TODO implement test case for empty date param (now)

# "2025-XX-XXT14:00:00Z"


# 1) viernes 5:00 pm COL + 1h → lunes 9:00 am COL = 14:00Z
def test_1_viernes_5pm_mas_1h():
    r = test_client.get(C, params={"date": "2025-01-03T2:00:00Z", "hours": 1})
    assert r.status_code == 200
    assert r.json() == {"date": "2025-01-07T13:00:00Z"}


# 2) sabado 2:00 pm COL + 1h → lunes 9:00 am COL = 14:00Z
def test_2_sabado_2pm_mas_1h():
    r = test_client.get(C, params={"date": "2025-01-04T19:00:00Z", "hours": 1})
    assert r.status_code == 200
    assert r.json() == {"date": "2025-01-07T13:00:00Z"}


# 3) martes 3:00 pm COL + 1d + 4h → jueves 10:00 am COL = 15:00Z
def test_3_martes_3pm_mas_1d_4h():
    r = test_client.get(
        C, params={"date": "2025-01-07T20:00:00Z", "days": 1, "hours": 4}
    )
    assert r.status_code == 200
    assert r.json() == {"date": "2025-01-09T15:00:00Z"}


# 4) domingo 6:00 pm COL + 1d → lunes 5:00 pm COL = 22:00Z
def test_4_domingo_6pm_mas_1d():
    r = test_client.get(C, params={"date": "2025-01-05T23:00:00Z", "days": 1})
    assert r.status_code == 200
    assert r.json() == {"date": "2025-01-07T21:00:00Z"}


# 5) laboral 8:00 am COL + 8h → mismo día 5:00 pm COL = 22:00Z
def test_5_laboral_8am_mas_8h():
    r = test_client.get(C, params={"date": "2025-01-06T13:00:00Z", "hours": 8})
    assert r.status_code == 200
    assert r.json() == {"date": "2025-01-07T21:00:00Z"}


# 6) laboral 8:00 am COL + 1d → siguiente día 8:00 am COL = 13:00Z
def test_6_laboral_8am_mas_1d():
    r = test_client.get(C, params={"date": "2025-01-06T13:00:00Z", "days": 1})
    assert r.status_code == 200
    assert r.json() == {"date": "2025-01-07T21:00:00Z"}


# 7) laboral 12:30 pm COL + 1d → siguiente día 12:00 pm COL = 17:00Z
def test_7_laboral_12_30_mas_1d():
    r = test_client.get(C, params={"date": "2025-01-06T17:30:00Z", "days": 1})
    assert r.status_code == 200
    assert r.json() == {"date": "2025-01-07T21:00:00Z"}


# 8) laboral **11:30 am** COL + 3h → 3:30 pm COL = 20:30Z
def test_8_laboral_11_30am_mas_3h():
    r = test_client.get(C, params={"date": "2025-01-06T16:30:00Z", "hours": 3})
    assert r.status_code == 200
    assert r.json() == {"date": "2025-01-07T15:00:00Z"}


# 9) con festivos (17–18 abr) — 10 abr 10:00 am COL + 5d + 4h → 21 abr 3:00 pm COL = 20:00Z
def test_9_con_festivos():
    r = test_client.get(
        C, params={"date": "2025-04-10T15:00:00Z", "days": 5, "hours": 4}
    )
    assert r.status_code == 200
    assert r.json() == {"date": "2025-04-21T20:00:00Z"}


def test_10_broken_query():
    r = test_client.get(C + "?asdasd")
    assert r.status_code == 400
    assert r.json() == {"error": "InvalidParameters"}
