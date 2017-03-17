from app import db


class Contributions(db.Model):
    version = db.Column(db.Integer)
    status = db.Column(db.String(35))

    idpoi = db.Column(db.Integer, db.ForeignKey(
        'pois.id'), primary_key=True, autoincrement=True)
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

    def __init__(self, pois=None, fields=None, values=None):
        self.pois = pois
        self.fields = fields
        self.values = values

    def __repr__(self):
        return '<Contributions {}>'.format(self.pois.id + " " + self.fields.name + " " + self.values.value)

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
    typespoi = db.relationship('Typespois', backref='generaltypes', lazy='dynamic')


class Typespois(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    name_fr = db.Column(db.String(80))
    name_en = db.Column(db.String(80))
    name_es = db.Column(db.String(80))
    name_de = db.Column(db.String(80))
    name_it = db.Column(db.String(80))
    generaltypes_id = db.Column(db.Integer, db.ForeignKey('generaltypes.id'), nullable=False)
    pois = db.relationship('Pois', backref='typespois', lazy='dynamic')


class Pois(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tour_id = db.Column(db.Integer)
    typespois_id = db.Column(db.Integer, db.ForeignKey('typespois.id'), nullable=False)


    fields = db.relationship('Fields', secondary='contributions',
                             backref=db.backref('pois', lazy='dynamic'))
    values = db.relationship('Values', secondary='contributions',
                             backref=db.backref('pois', lazy='dynamic'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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


class Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text)
    createddate = db.Column(db.Date)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(35))
    firstname = db.Column(db.String(35))
    email = db.Column(db.String(35))
    picture = db.Column(db.String(35))
    values = db.relationship('Values', backref='users', lazy='dynamic')
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    accounts_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))


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