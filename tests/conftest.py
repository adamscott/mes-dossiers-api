import pytest
from testing.postgresql import Postgresql

from mesdossiers import create_app
from mesdossiers.database import db as _db
from mesdossiers.config import TestingConfig as _TestingConfig


class TestingConfig(_TestingConfig):
    pass


@pytest.yield_fixture(scope='session')
def app():
    with Postgresql() as postgresql:
        _app = create_app(
            config_object=TestingConfig,
            settings_override={
                'SQLALCHEMY_DATABASE_URI': postgresql.url()
            }
        )
        ctx = _app.app_context()
        ctx.push()

        yield _app

        ctx.pop()


@pytest.fixture(scope='session')
def testapp(app):
    return app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()
