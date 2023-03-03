import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)



class Candidat(Base):
    __tablename__ = "candidates"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String(length=40))
    last_name = sq.Column(sq.String(length=40))
    link = sq.Column(sq.String(length=1000))
    photos = sq.Column(sq.String(length=1000))
    id_user = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)

    user = relationship(User, backref="candidat")

class Favorit(Base):
    __tablename__ = "favorites"
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String(length=40))
    last_name = sq.Column(sq.String(length=40))
    link = sq.Column(sq.String(length=1000))
    photos = sq.Column(sq.String(length=1000))
    id_user = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)

    user = relationship(User, backref="favorit")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)