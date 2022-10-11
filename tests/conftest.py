import pytest
from app import app as fsk

@pytest.fixture()
def app():
    # other setup can go here

    yield fsk

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()