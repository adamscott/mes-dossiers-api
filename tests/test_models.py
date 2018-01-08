from mesdossiers.models import User, Group


class TestUser:

    def test_init(self, app, db, session):
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

            session.add(john)
            session.add(oliver)
            session.commit()

            print(User.query.filter(
                User.groups.any(Group.name == 'Admin')
            ).all())

            assert len(User.query.filter(
                User.groups.any(Group.name == 'Admin')
            ).all()) == 2

            print(User.query.filter(User.username == 'john01').one())

    def test_auth(self, app):
        with app.app_context():
            john = User.query.filter(User.username == 'john01').one()
            print('Auth token for john: ', john.encode_auth_token())
