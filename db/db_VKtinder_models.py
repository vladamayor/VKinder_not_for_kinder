import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)

    def __str__(self):
        return f'{self.id}, {self.user_id}'


class Candidat(Base):
    __tablename__ = "candidates"

    id = sq.Column(sq.Integer, primary_key=True)
    candidate_id = sq.Column(sq.Integer, unique=True)
    first_last_name = sq.Column(sq.String(length=40))
    link = sq.Column(sq.String(length=1000))
    photos = sq.Column(sq.String(length=1000))
    id_user = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)

    user = relationship(User, backref="candidat")

    def __str__(self):
        return f'{self.candidate_id}, {self.first_last_name}, {self.link}, {self.photos}'


class Favorit(Base):
    __tablename__ = "favorites"
    id = sq.Column(sq.Integer, primary_key=True)
    favorite_id = sq.Column(sq.Integer, unique=True)
    first_last_name = sq.Column(sq.String(length=40))
    link = sq.Column(sq.String(length=1000))
    photos = sq.Column(sq.String(length=1000))
    id_user = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)

    user = relationship(User, backref="favorit")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
