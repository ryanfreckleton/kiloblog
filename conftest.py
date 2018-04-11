import pytest
import kiloblog


@pytest.fixture
def app():
    kiloblog.app.testing = True
    kiloblog.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    kiloblog.app.config['WTF_CSRF_ENABLED'] = False
    kiloblog.db.drop_all()
    kiloblog.db.create_all()
    return kiloblog.app
