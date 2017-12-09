from datetime import datetime
from enum import Enum
from .database import db


user_group = db.Table(
    'user_group',
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.ForeignKey('group.id'), primary_key=True)
)

case_document = db.Table(
    'case_document',
    db.Column('case_id', db.ForeignKey('case.id'), primary_key=True),
    db.Column('document_id', db.ForeignKey('document.id'), primary_key=True)
)

file_document = db.Table(
    'file_document',
    db.Column('file_id', db.ForeignKey('file.id'), primary_key=True),
    db.Column('document_id', db.ForeignKey('document.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    groups = db.relationship("Group", secondary=user_group, back_populates="users")

    def __repr__(self):
        return '<User %r>' % self.username


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    emails = db.relationship("ProfileEmail", back_populates="profile")
    addresses = db.relationship("ProfileAddress", back_populates="profile")
    parties = db.relationship("Party", back_populates="profile")

    def __repr__(self):
        return '<Profile {} {}>'.format(self.first_name, self.last_name)


class ProfileEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    email = db.Column(db.String(50), nullable=False)

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    profile = db.relationship("Profile", back_populates="emails")

    def __repr__(self):
        return '<ProfileEmail {} (profile: {})>'.format(self.email, self.profile)


class ProfileAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    address_1 = db.Column(db.String(150))
    address_2 = db.Column(db.String(150))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    postal_code = db.Column(db.String(15))
    country = db.Column(db.String(50))

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    profile = db.relationship("Profile", back_populates="addresses")

    address_type_id = db.Column(db.Integer, db.ForeignKey("profile_address_type.id"))
    address_type = db.relationship("ProfileAddressType", back_populates="profile_addresses")

    def __repr__(self):
        return '<ProfileAddress {} (profile: {})>'.format(self.address_1, self.profile)


class ProfileAddressTypeEnum(Enum):
    OTHER = 1
    HOME = 2
    OFFICE = 3


class ProfileAddressType(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    address_type = db.Column(db.Enum(ProfileAddressTypeEnum), nullable=False)

    profile_addresses = db.relationship("ProfileAddress", order_by="ProfileAddress.id", back_populates="address_type")

    def __repr__(self):
        return '<ProfileAddressType {}>'.format(self.address_type)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), nullable=False)

    users = db.relationship("User", secondary=user_group, back_populates="groups")

    def __repr__(self):
        return '<Group {}>'.format(self.name)


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    files = db.relationship("File", order_by="File.id", back_populates="case")
    documents = db.relationship("Document", secondary=case_document, back_populates="cases")

    def __repr__(self):
        return '<Case {}>'.format(self.id)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    file_number = db.Column(db.String(50), nullable=False)
    appeal_file_number = db.Column(db.String(50))

    case_id = db.Column(db.Integer, db.ForeignKey("case.id"))
    case = db.relationship("Case", back_populates="files")

    status_id = db.Column(db.Integer, db.ForeignKey("file_status.id"))
    status = db.relationship("FileStatus", back_populates="files")

    parties = db.relationship("Party", order_by="Party.id", back_populates="file")
    documents = db.relationship("Document", secondary=file_document, back_populates="files")
    events = db.relationship("FileEvent", order_by="FileEvent.event_date", back_populates="file")

    def __repr__(self):
        return '<File {} (case: {})>'.format(self.file_number, self.case)


class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    type = db.Column(db.String(50), nullable=False)

    file_id = db.Column(db.Integer, db.ForeignKey("file.id"))
    file = db.relationship("File", back_populates="parties")

    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    profile = db.relationship("Profile", back_populates="parties")

    def __repr__(self):
        return '<Party (profile: {}) (file: {})>'.format(self.profile, self.file)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    file_name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

    cases = db.relationship("Case", secondary=case_document, back_populates="documents")
    files = db.relationship("File", secondary=file_document, back_populates="documents")

    def __repr__(self):
        return '<Document {}>'.format(self.file_name)


class FileEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    title = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)

    file_id = db.Column(db.Integer, db.ForeignKey("file.id"))
    file = db.relationship("File", back_populates="events")

    type_id = db.Column(db.Integer, db.ForeignKey("file_event_type.id"))
    type = db.relationship("FileEventType", back_populates="events")

    def __repr__(self):
        return '<FileEvent {} (file: {})>'.format(self.title, self.file)


class FileEventTypeEnum(Enum):
    RENDEZ_VOUS = 1


class FileEventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.Enum(FileEventTypeEnum), nullable=False)

    events = db.relationship("FileEvent", order_by="FileEvent.event_date", back_populates="type")

    def __repr__(self):
        return '<FileEventType {}>'.format(self.type)


class FileStatusEnum(Enum):
    OPEN = 1
    ACTIVE = 2
    STANDBY = 3
    CLOSED = 4


class FileStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.Enum(FileStatusEnum), nullable=False)

    files = db.relationship("File", order_by="File.file_number", back_populates="status")

    def __repr__(self):
        return '<FileStatus {}>'.format(self.status)
