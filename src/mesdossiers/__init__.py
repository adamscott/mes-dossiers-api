from flask import Flask
from flask_restful import Api

from .resources import Cases
from .config import Config


def create_app(name=__name__.split('.')[0], config_object=Config, settings_override=None):
    app = Flask(name)
    app.config.from_object(config_object)

    if settings_override is not None:
        for key, value in settings_override.items():
            app.config[key] = value

    from .database import db
    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()

    api = Api(app)
    api.add_resource(Cases, '/')

    return app


app = create_app()


def main():
    pass


if __name__ == "__main__":
    main()
