from ..app import create_app
from ..app.models import *
from werkzeug.security import generate_password_hash, check_password_hash

def test_basic_routes_exist(test_client):
    for route in ["/login", "/register"]:
        assert test_client.get(route).status_code == 200

def test_protected_views_return_unauthorised(test_client):
    for route in ["/dashboard"]:
        response = test_client.get(route, follow_redirects=True)
        assert test_client.get(route).status_code == 302
        assert response.status_code == 200
        assert "<title>Login - Online Movie Store Application</title>" in str(response.data)

    account = Account(\
        first_name="Dion",\
        last_name="Misic",\
        email="dion.misic@gmail.com",\
        password=generate_password_hash("ISD", method='sha256'),\
        street_address="ISD Building 01",\
        postcode="2222",\
        is_staff=False\
    )

    db.session.add(account)
    db.session.commit()

    test_client.post("/do-login", data={"email": "dion.misic@gmail.com", "password": "ISD"})

    for route in ["/dashboard"]:
        response = test_client.get(route, follow_redirects=True)
        assert response.status_code == 200
        assert "<title>Dashboard - Online Movie Store Application</title>" in str(response.data)

    test_client.get("/logout")
       
    for route in ["/dashboard"]:
        response = test_client.get(route, follow_redirects=True)
        assert test_client.get(route).status_code == 302
        assert response.status_code == 200
        assert "<title>Login - Online Movie Store Application</title>" in str(response.data)
