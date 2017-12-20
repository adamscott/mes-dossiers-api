from datetime import datetime
from enum import Enum
from .database import db

from typing import List


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

    def __init__(self, username: str, email: str, password: str, groups: List['Group']=None, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.email = email
        self.password = password
        if groups is not None:
            self.groups = groups

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    emails = db.relationship("ProfileEmail", back_populates="profile")
    addresses = db.relationship("ProfileAddress", back_populates="profile")
    parties = db.relationship("Party", back_populates="profile")

    def __init__(self, first_name: str, last_name: str, emails: List['ProfileEmail']=None,
                 addresses: List['ProfileAddress']=None, parties: List['Party']=None, **kwargs):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        if emails is not None:
            self.emails = emails
        if addresses is not None:
            self.addresses = addresses
        if parties is not None:
            self.parties = parties

    def __repr__(self):
        return '<Profile {} {}>'.format(self.first_name, self.last_name)


class ProfileEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    email = db.Column(db.String(50), nullable=False)

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    profile = db.relationship("Profile", back_populates="emails")

    def __init__(self, email: str, profile: 'Profile'=None, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        if profile is not None:
            self.profile = profile

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

    def __init__(self, address_1: str=None, address_2: str=None, city: str=None, state: str=None,
                 postal_code: str=None, country: str=None, profile: 'Profile'=None,
                 address_type: 'ProfileAddressType'=None, **kwargs):
        super().__init__(**kwargs)
        if address_1 is not None:
            self.address_1 = address_1
        if address_2 is not None:
            self.address_2 = address_2
        if city is not None:
            self.city = city
        if state is not None:
            self.state = state
        if postal_code is not None:
            self.postal_code = postal_code
        if country is not None:
            self.country = country
        if profile is not None:
            self.profile = profile
        if address_type is not None:
            self.address_type = address_type

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

    def __init__(self, address_type: 'ProfileAddressTypeEnum',
                 profile_addresses: List['ProfileAddress']=None, **kwargs):
        super().__init__(**kwargs)
        self.address_type = address_type
        if profile_addresses is not None:
            self.profile_addresses = profile_addresses

    def __repr__(self):
        return '<ProfileAddressType {}>'.format(self.address_type)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), nullable=False)

    users = db.relationship("User", secondary=user_group, back_populates="groups")

    def __init__(self, name: str, users: List['User']=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        if users is not None:
            self.users = users

    def __repr__(self):
        return '<Group {}>'.format(self.name)


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    files = db.relationship("File", order_by="File.id", back_populates="case")
    documents = db.relationship("Document", secondary=case_document, back_populates="cases")

    def __init__(self, files: List['File']=None, documents: List['Document']=None, **kwargs):
        super().__init__(**kwargs)
        if files is not None:
            self.files = files
        if documents is not None:
            self.documents = documents

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

    def __init__(self, file_number: str, appeal_file_number: str=None, case: 'Case'=None,
                 status: 'FileStatus'=None, parties: List['Party']=None, documents: List['Document']=None,
                 events: List['FileEvent']=None, **kwargs):
        super().__init__(**kwargs)
        self.file_number = file_number
        if appeal_file_number is not None:
            self.appeal_file_number = appeal_file_number
        if case is not None:
            self.case = case
        if status is not None:
            self.status = status
        if parties is not None:
            self.parties = parties
        if documents is not None:
            self.documents = documents
        if events is not None:
            self.events = events

    def __repr__(self):
        return '<File {} (case: {})>'.format(self.file_number, self.case)


class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    name = db.Column(db.String(50), nullable=False)

    file_id = db.Column(db.Integer, db.ForeignKey("file.id"))
    file = db.relationship("File", back_populates="parties")

    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    profile = db.relationship("Profile", back_populates="parties")

    def __init__(self, name: str, file: 'File'=None, profile: 'Profile'=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        if file is not None:
            self.file = file
        if profile is not None:
            self.profile = profile

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

    def __init__(self, file_name: str, data: bytes, cases: List['Case']=None, files: List['File']=None, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_name
        self.data = data
        if cases is not None:
            self.cases = cases
        if files is not None:
            self.files = files

    def __repr__(self):
        return '<Document {}>'.format(self.file_name)


class FileEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    title = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.Text)

    file_id = db.Column(db.Integer, db.ForeignKey("file.id"))
    file = db.relationship("File", back_populates="events")

    file_event_type_id = db.Column(db.Integer, db.ForeignKey("file_event_type.id"))
    file_event_type = db.relationship("FileEventType", back_populates="events")

    def __init__(self, title: str, event_date: 'datetime', comment: str=None, file: 'File'=None,
                 file_event_type: 'FileEventType'=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.event_date = event_date
        if comment is not None:
            self.comment = comment
        if file is not None:
            self.file = file
        if file_event_type is not None:
            self.file_event_type = file_event_type

    def __repr__(self):
        return '<FileEvent {} (file: {})>'.format(self.title, self.file)


class FileEventTypeEnum(Enum):
    RENDEZ_VOUS = 1


class FileEventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Enum(FileEventTypeEnum), nullable=False)

    events = db.relationship("FileEvent", order_by="FileEvent.event_date", back_populates="file_event_type")

    def __init__(self, name: 'FileEventTypeEnum', events: List['FileEvent']=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        if events is not None:
            self.events = events

    def __repr__(self):
        return '<FileEventType {}>'.format(self.name)


class FileStatusEnum(Enum):
    OPEN = 1
    ACTIVE = 2
    STANDBY = 3
    CLOSED = 4


class FileStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.Enum(FileStatusEnum), nullable=False)

    files = db.relationship("File", order_by="File.file_number", back_populates="status")

    def __init__(self, status: 'FileStatusEnum', files: List['File']=None, **kwargs):
        super().__init__(**kwargs)
        self.status = status
        if files is not None:
            self.files = files

    def __repr__(self):
        return '<FileStatus {}>'.format(self.status)
