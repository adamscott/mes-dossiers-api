from . import config, models

from flask import Flask
from .database import db


def create_app(name=__name__, config_object=".config.Config", settings_override=None):
    app = Flask(name)
    app.config.from_object(config_object)

    if settings_override is not None:
        for key, value in settings_override.items():
            app.config[key] = value

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()

    return app
