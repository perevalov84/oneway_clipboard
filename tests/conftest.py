import pytest
from oneway_clipboard.flask.app import create_app

@pytest.fixture
def app():
    test_config = {
        "TESTING":True,
    }
    app = create_app(test_config=test_config)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()