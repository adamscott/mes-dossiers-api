from flask_sqlalchemy import SQLAlchemy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union
    import sqlalchemy
    from sqlalchemy import orm


db = SQLAlchemy()  # type: Union[SQLAlchemy, sqlalchemy, orm]
