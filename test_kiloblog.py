import pytest

import kiloblog


def setup_module():
    kiloblog.app.testing = True
    kiloblog.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    kiloblog.db.create_all()


@pytest.fixture
def client():
    return kiloblog.app.test_client()


class TestIndex:
    def test_get(self, client):
        assert client.get('/').status == '200 OK'
