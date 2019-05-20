from ..app import app

def test_basicroutes_exist():
    with app.test_client() as c:
        for route in ["/login", "/register"]:
            response = c.get(route)
            assert response.status_code == 200