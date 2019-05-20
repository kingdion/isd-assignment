from ..app import app, db
from ..app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

some_engine = create_engine('postgresql://postgres:isd_password@localhost:5432/isd')
Session = sessionmaker(bind=some_engine)
session = Session()
session.begin(subtransactions=True)

def test_basic_routes_exist():
    with app.test_client() as test_client:
        for route in ["/login", "/register"]:
            assert test_client.get(route).status_code == 200

def test_protected_views_return_unauthorised():
    with app.test_client() as test_client:
        for route in ["/dashboard"]:
            assert test_client.get(route).status_code == 302
            assert test_client.get(route, follow_redirects=True).status_code == 200
    
        account = Account(\
            first_name="Dion",\
            last_name="Misic",\
            email="dion.misic@gmail.com",\
            password=generate_password_hash("ISD", method='sha256'),\
            street_address="ISD Building 01",\
            postcode="2222",\
            is_staff=False\
        )

        session.add(account)
        session.commit()

        test_client.post("/do-login", data={"email": "dion.misic@gmail.com", "password": "ISD"})

        for route in ["/dashboard"]:
            assert test_client.get(route, follow_redirects=True).status_code == 200

        session.rollback()
        session.close()
    