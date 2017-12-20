"""
Inspired by:
https://github.com/sloria/cookiecutter-flask/blob/master/%7B%7Bcookiecutter.app_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/database.py
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union
    import sqlalchemy
    from sqlalchemy import orm


db = SQLAlchemy()  # type: Union[SQLAlchemy, sqlalchemy, orm]

ForeignKey = db.ForeignKey
Table = db.Table

String = db.String
Integer = db.Integer
DateTime = db.DateTime
Enum = db.Enum

Column = db.Column
relationship = db.relationship


class CRUDMixin:
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePKMixin:
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None


class TimestampMixin:
    """A mixin that adds timestamp columns."""

    __table_args__ = {'extend_existing': True}

    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow)
