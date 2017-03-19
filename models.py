from app import db
from sqlalchemy import Date
from datetime import date

class Contributions(db.Model):
    version = db.Column(db.Integer)
    status = db.Column(db.String(35))

    idpoi = db.Column(db.Integer, db.ForeignKey(
        'pois.id'), primary_key=True)
    idfield = db.Column(db.Integer, db.ForeignKey(
        'fields.id'), primary_key=True)
    idvalue = db.Column(db.Integer, db.ForeignKey(
        'values.id'), primary_key=True)

    pois = db.relationship("Pois", backref=db.backref(
        "contributions", cascade="all, delete-orphan"))
    fields = db.relationship("Fields", backref=db.backref(
        "contributions", cascade="all, delete-orphan"))
    values = db.relationship("Values", backref=db.backref(
        "contributions", cascade="all, delete-orphan"))

    def __init__(self, version=None, status=None, pois=None, fields=None, values=None):
        self.version = version
        self.status = status
        self.pois = pois
        self.fields = fields
        self.values = values

    def __repr__(self):
        return '<Contributions {}>'.format(self.pois.version + " " +self.pois.status + " " +self.pois.id + " " + self.fields.name + " " + self.values.value)


class Comments(db.Model):
    message = db.Column(db.Text)
    title = db.Column(db.String(50))
    createdDate = db.Column(db.Date)
    iduser = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    idpoi = db.Column(db.Integer, db.ForeignKey(
        'pois.id'), primary_key=True)

    users = db.relationship("Users", backref=db.backref(
        "comments", cascade="all, delete-orphan"))
    pois = db.relationship("Pois", backref=db.backref(
        "comments", cascade="all, delete-orphan"))


class Rewards(db.Model):
    idaward = db.Column(db.Integer, db.ForeignKey(
        'awards.id'), primary_key=True)
    iduser = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)

    award = db.relationship("Awards", backref=db.backref(
        "rewards", cascade="all, delete-orphan"))
    users = db.relationship("Users", backref=db.backref(
        "rewards", cascade="all, delete-orphan"))


class Generaltypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    name_fr = db.Column(db.String(80))
    name_en = db.Column(db.String(80))
    name_es = db.Column(db.String(80))
    name_de = db.Column(db.String(80))
    name_it = db.Column(db.String(80))
    typespoi = db.relationship(
        'Typespois', backref='generaltypes', lazy='dynamic')


class Typespois(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    name_fr = db.Column(db.String(80))
    name_en = db.Column(db.String(80))
    name_es = db.Column(db.String(80))
    name_de = db.Column(db.String(80))
    name_it = db.Column(db.String(80))
    generaltypes_id = db.Column(db.Integer, db.ForeignKey(
        'generaltypes.id'), nullable=False)
    pois = db.relationship('Pois', backref='typespois', lazy='dynamic')


class Pois(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, nullable=False)
    typespois_id = db.Column(db.Integer, db.ForeignKey(
        'typespois.id'), nullable=False)

    fields = db.relationship('Fields', secondary='contributions',
                             viewonly=True)
    values = db.relationship('Values', secondary='contributions',
                             viewonly=True)

    def __init__(self, required, optional):
        self.tour_id = required['tour_id']
        self.typespois_id = required['typespois_id']
        if 'values' in optional:
            self.values = optional['values']
        if 'fields' in optional:
            self.fields = required['fields']

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def getCol():
        data = []
        for c in Pois.__table__.columns:
            if c.name not in ['id']:
                data.append(c.name)
        return data

    def getColRequired():
        data = []
        for c in Pois.__table__.columns:
            if c.name not in ['id', 'values', 'fields'] and not c.nullable:
                data.append(c.name)
        return data

    def getColOptional():
        data = []
        for c in Pois.__table__.columns:
            if c.name not in ['id'] and c.nullable:
                data.append(c.name)
        return data


class Types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    size = db.Column(db.Integer)
    fields = db.relationship('Fields', backref='types', lazy='dynamic')


class Fields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pos = db.Column(db.Integer)
    name = db.Column(db.String(80))
    required = db.Column(db.Boolean)
    types_id = db.Column(db.Integer, db.ForeignKey('types.id'))

    pois = db.relationship(
        'Pois',
        secondary='contributions',
        viewonly=True
    )
    values = db.relationship(
        'Values',
        secondary='contributions',
        viewonly=True
    )

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.pois = []
        self.values = []


class Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text)
    createddate = db.Column(db.Date)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    fields = db.relationship(
        'Fields',
        secondary='contributions',
		viewonly=True
    )
    pois = db.relationship(
        'Pois',
        secondary='contributions',
		viewonly=True
    )

    def __init__(self, value):
        self.value = value
        self.createddate = date.today()
        self.fields = []
        self.pois = []


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(35))
    firstname = db.Column(db.String(35))
    email = db.Column(db.String(35))
    picture = db.Column(db.String(35))

    values = db.relationship('Values', backref='users', lazy='dynamic')
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    accounts_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __init__(self, lastname, firstname, email):
        self.lastname = lastname
        self.firstname = firstname
        self.email = email

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('Users', backref='categories', lazy='dynamic')


class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    users = db.relationship('Users', backref='accounts', lazy='dynamic')


class Awards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typeAward = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(25), nullable=False)

db.create_all()
db.session.commit()
