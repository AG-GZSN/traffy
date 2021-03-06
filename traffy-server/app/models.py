from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db


Base = declarative_base()

class RegistrationKey(Base):
    __tablename__ = "registration_key"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean(True), nullable=False)
    eula_accepted = db.Column(db.Boolean(False), nullable=False)
    identity = db.Column(db.Integer, db.ForeignKey("identity.id"))
    enable_accounting = db.Column(db.Boolean(True), nullable=False)
    daily_topup_volume = db.Column(db.BigInteger, nullable=True)
    max_volume = db.Column(db.BigInteger, nullable=True)
    block_traffic = db.Column(db.Boolean(False), nullable=False)
    ingress_speed = db.Column(db.Integer, nullable=True)
    egress_speed = db.Column(db.Integer, nullable=True)
    
    def __init__(self, key, identity):
        self.key = key
        self.created_on = datetime.now()
        self.active = True
        self.eula_accepted = False
        self.identity = identity
        self.enable_accounting = True
        self.daily_topup_volume = None
        self.max_volume = None
        self.block_traffic = False
        self.ingress_speed = None
        self.egress_speed = None
    
    def __repr__(self):
        return "<RegistrationKey %r>" % self.key

class MacAddress(Base):
    __tablename__ = "mac_address"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(25), unique=True, nullable=False)
    user_agent = db.Column(db.String(500), unique=False, nullable=True)
    first_known_since = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, address, user_agent, first_known_since):
        self.address = address
        self.user_agent = user_agent
        self.first_known_since = first_known_since
    
    def __repr__(self):
        return "<MacAddress %r>" % self.address

class IpAddress(Base):
    __tablename__ = "ip_address"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_v4 = db.Column(db.String(15), unique=True, nullable=False)
    address_v6 = db.Column(db.String(100), unique=True, nullable=True)
    
    def __init__(self, address_v4, address_v6):
        self.address_v4 = address_v4
        self.address_v6 = address_v6
    
    def __repr__(self):
        return "<IpAddress %r>" % self.address_v4

class Identity(Base):
    __tablename__ = "identity"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    mail = db.Column(db.String(50), unique=False, nullable=False)
    room = db.Column(db.String(20), unique=True, nullable=False)
    
    def __init__(self, first_name, last_name, mail, room):
        self.first_name = first_name
        self.last_name = last_name
        self.mail = mail
        self.room = room
    
    def __repr__(self):
        return "<Identity %r>" % self.first_name

class Traffic(Base):
    __tablename__ = "traffic"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reg_key = db.Column(db.Integer, db.ForeignKey("registration_key.id"))
    timestamp = db.Column(db.DateTime, nullable=False)
    credit = db.Column(db.BigInteger, nullable=False)
    ingress = db.Column(db.BigInteger, nullable=False)
    egress = db.Column(db.BigInteger, nullable=False)
    ingress_shaped = db.Column(db.BigInteger, nullable=False)
    egress_shaped = db.Column(db.BigInteger, nullable=False)
    
    def __init__(self, reg_key, timestamp, credit, ingress, egress, ingress_shaped, egress_shaped):
        self.reg_key = reg_key
        self.timestamp = timestamp
        self.credit = credit
        self.ingress = ingress
        self.egress = egress
        self.ingress_shaped = ingress_shaped
        self.egress_shaped = egress_shaped
    
    def __repr__(self):
        return "<Traffic %r>" % self.reg_key

class Voucher(Base):
    __tablename__ = "voucher"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=True)
    all_users = db.Column(db.Boolean(False), nullable=False)
    
    def __init__(self, code, valid_until, multiple_users):
        self.code = code
        self.valid_until = valid_until
        self.multiple_users = multiple_users
    
    def __repr__(self):
        return "<Voucher %r>" % self.code

class VoucherUser(Base):
    __tablename__ = "voucher_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Integer, db.ForeignKey("voucher.id"))
    reg_key = db.Column(db.Integer, db.ForeignKey("registration_key.id"))
    date = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, code, reg_key, date):
        self.code = code
        self.reg_key = reg_key
        self.date = date
    
    def __repr__(self):
        return "<VoucherUser %r>" % self.code

class AddressPair(Base):
    __tablename__ = "address_pair"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reg_key = db.Column(db.Integer, db.ForeignKey("registration_key.id"))
    mac_address = db.Column(db.Integer, db.ForeignKey("mac_address.id"))
    ip_address = db.Column(db.Integer, db.ForeignKey("ip_address.id"))
    
    def __init__(self, reg_key, mac_address, ip_address):
        self.reg_key = reg_key
        self.mac_address = mac_address
        self.ip_address = ip_address
    
    def __repr__(self):
        return "<AddressPairs %r>" % self.reg_key

def create_all(engine):
    Base.metadata.create_all(engine)

