import enum

from passlib.hash import sha512_crypt

from datetime import datetime
from .database import db, \
                      Column, relationship, ForeignKey, Table, \
                      String, Integer, DateTime, Enum, \
                      Model, SurrogatePKMixin, TimestampMixin

from typing import List

from .auth import encode_auth_token as _encode_auth_token


user_group = Table(
    'user_group',
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('group_id', ForeignKey('group.id'), primary_key=True)
)

case_document = Table(
    'case_document',
    Column('case_id', ForeignKey('case.id'), primary_key=True),
    Column('document_id', ForeignKey('document.id'), primary_key=True)
)

file_document = Table(
    'file_document',
    Column('file_id', ForeignKey('file.id'), primary_key=True),
    Column('document_id', ForeignKey('document.id'), primary_key=True)
)


class User(SurrogatePKMixin, TimestampMixin, Model):
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    profile_id = Column(Integer, ForeignKey("profile.id"))
    profile = relationship("Profile")

    groups = relationship("Group", secondary=user_group, back_populates="users")

    def __init__(self, username: str, email: str, password: str, profile: 'Profile'=None,
                 groups: List['Group']=None, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.email = email
        self.password = sha512_crypt(password)
        if groups is not None:
            self.groups = groups
        if profile is not None:
            self.profile = profile

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def encode_auth_token(self):
        return _encode_auth_token(self.id)


class Profile(SurrogatePKMixin, TimestampMixin, Model):
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    emails = relationship("ProfileEmail", back_populates="profile")
    addresses = relationship("ProfileAddress", back_populates="profile")
    parties = relationship("Party", back_populates="profile")

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


class ProfileEmail(SurrogatePKMixin, TimestampMixin, Model):
    email = Column(String(50), nullable=False)

    profile_id = Column(Integer, ForeignKey('profile.id'))
    profile = relationship("Profile", back_populates="emails")

    def __init__(self, email: str, profile: 'Profile'=None, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        if profile is not None:
            self.profile = profile

    def __repr__(self):
        return '<ProfileEmail {} (profile: {})>'.format(self.email, self.profile)


class ProfileAddress(SurrogatePKMixin, TimestampMixin, Model):
    address_1 = Column(String(150))
    address_2 = Column(String(150))
    city = Column(String(50))
    state = Column(String(50))
    postal_code = Column(String(15))
    country = Column(String(50))

    profile_id = Column(Integer, ForeignKey('profile.id'))
    profile = relationship("Profile", back_populates="addresses")

    address_type_id = Column(Integer, ForeignKey("profile_address_type.id"))
    address_type = relationship("ProfileAddressType", back_populates="profile_addresses")

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


class ProfileAddressTypeEnum(enum.Enum):
    OTHER = 1
    HOME = 2
    OFFICE = 3


class ProfileAddressType(SurrogatePKMixin, Model):
    address_type = Column(Enum(ProfileAddressTypeEnum), nullable=False)

    profile_addresses = relationship("ProfileAddress", order_by="ProfileAddress.id", back_populates="address_type")

    def __init__(self, address_type: 'ProfileAddressTypeEnum',
                 profile_addresses: List['ProfileAddress']=None, **kwargs):
        super().__init__(**kwargs)
        self.address_type = address_type
        if profile_addresses is not None:
            self.profile_addresses = profile_addresses

    def __repr__(self):
        return '<ProfileAddressType {}>'.format(self.address_type)


class Group(SurrogatePKMixin, TimestampMixin, Model):
    name = Column(String(30), nullable=False)

    users = relationship("User", secondary=user_group, back_populates="groups")

    def __init__(self, name: str, users: List['User']=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        if users is not None:
            self.users = users

    def __repr__(self):
        return '<Group {}>'.format(self.name)


class Case(SurrogatePKMixin, TimestampMixin, Model):
    files = relationship("File", order_by="File.id", back_populates="case")
    documents = relationship("Document", secondary=case_document, back_populates="cases")

    def __init__(self, files: List['File']=None, documents: List['Document']=None, **kwargs):
        super().__init__(**kwargs)
        if files is not None:
            self.files = files
        if documents is not None:
            self.documents = documents

    def __repr__(self):
        return '<Case {}>'.format(self.id)


class File(SurrogatePKMixin, TimestampMixin, Model):
    file_number = Column(String(50), nullable=False)
    appeal_file_number = Column(String(50))

    case_id = Column(Integer, ForeignKey("case.id"))
    case = relationship("Case", back_populates="files")

    status_id = Column(Integer, ForeignKey("file_status.id"))
    status = relationship("FileStatus", back_populates="files")

    parties = relationship("Party", order_by="Party.id", back_populates="file")
    documents = relationship("Document", secondary=file_document, back_populates="files")
    events = relationship("FileEvent", order_by="FileEvent.event_date", back_populates="file")

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


class Party(SurrogatePKMixin, TimestampMixin, Model):
    name = Column(String(50), nullable=False)

    file_id = Column(Integer, ForeignKey("file.id"))
    file = relationship("File", back_populates="parties")

    profile_id = Column(Integer, ForeignKey("profile.id"))
    profile = relationship("Profile", back_populates="parties")

    def __init__(self, name: str, file: 'File'=None, profile: 'Profile'=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        if file is not None:
            self.file = file
        if profile is not None:
            self.profile = profile

    def __repr__(self):
        return '<Party (profile: {}) (file: {})>'.format(self.profile, self.file)


class Document(SurrogatePKMixin, TimestampMixin, Model):
    file_name = Column(String(100), nullable=False)
    data = Column(db.LargeBinary, nullable=False)

    cases = relationship("Case", secondary=case_document, back_populates="documents")
    files = relationship("File", secondary=file_document, back_populates="documents")

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


class FileEvent(SurrogatePKMixin, TimestampMixin, Model):
    title = Column(String(100), nullable=False)
    event_date = Column(DateTime, nullable=False)
    comment = Column(db.Text)

    file_id = Column(Integer, ForeignKey("file.id"))
    file = relationship("File", back_populates="events")

    file_event_type_id = Column(Integer, ForeignKey("file_event_type.id"))
    file_event_type = relationship("FileEventType", back_populates="events")

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


class FileEventTypeEnum(enum.Enum):
    RENDEZ_VOUS = 1


class FileEventType(SurrogatePKMixin, TimestampMixin, Model):
    name = Column(Enum(FileEventTypeEnum), nullable=False)

    events = relationship("FileEvent", order_by="FileEvent.event_date", back_populates="file_event_type")

    def __init__(self, name: 'FileEventTypeEnum', events: List['FileEvent']=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        if events is not None:
            self.events = events

    def __repr__(self):
        return '<FileEventType {}>'.format(self.name)


class FileStatusEnum(enum.Enum):
    OPEN = 1
    ACTIVE = 2
    STANDBY = 3
    CLOSED = 4


class FileStatus(SurrogatePKMixin, Model):
    status = Column(Enum(FileStatusEnum), nullable=False)

    files = relationship("File", order_by="File.file_number", back_populates="status")

    def __init__(self, status: 'FileStatusEnum', files: List['File']=None, **kwargs):
        super().__init__(**kwargs)
        self.status = status
        if files is not None:
            self.files = files

    def __repr__(self):
        return '<FileStatus {}>'.format(self.status)
