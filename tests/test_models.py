import pytest

from mesdossiers.database import db
from mesdossiers.models import User, Group

from .conftest import app


class TestUser:

    def test_init(self):
        with app.app_context():
            admin_group = Group(name="Admin")

            john = User(
                username="john01",
                email="john@example.org",
                password="pass",
                groups=[
                    admin_group
                ]
            )

            oliver = User(
                username="oliii",
                email="oliver@example.org",
                password="word",
                groups=[
                    admin_group
                ]
            )

            db.session.add(john)
            db.session.add(oliver)
            db.session.commit()

            alls = User.query.filter(
                User.groups.any(Group.name == 'Admin')
            ).all()

            print(alls)
