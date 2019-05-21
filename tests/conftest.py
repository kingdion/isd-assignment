import pytest
from .. import app
from ..app.models import *

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    testing_client = app.test_client()

    with app.app_context():
        db.session.begin_nested()
        db.create_all()

        yield testing_client

        db.session.rollback()
        db.session.close()
