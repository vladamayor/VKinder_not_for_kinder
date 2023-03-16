import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer, unique=True)

    def __str__(self):
        return f"{self.id}, {self.user_vk_id}"


class Candidat(Base):
    __tablename__ = "candidates"

    id = sq.Column(sq.Integer, primary_key=True)
    candidate_vk_id = sq.Column(sq.Integer, unique=True)
    first_last_name = sq.Column(sq.String(length=100))
    link = sq.Column(sq.String(length=1000))
    id_user = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)

    user = relationship(User, backref="candidat")

    def __str__(self):
        return f"{self.id}, {self.candidate_vk_id}, {self.first_last_name}, {self.link}, {self.photos}, {self.id_user}"


class Favorit(Base):
    __tablename__ = "favorites"
    id = sq.Column(sq.Integer, primary_key=True)
    favorite_vk_id = sq.Column(sq.Integer, unique=True)
    first_last_name = sq.Column(sq.String(length=40))
    link = sq.Column(sq.String(length=1000))
    id_user = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)

    user = relationship(User, backref="favorit")

    def __str__(self):
        return f"{self.id}, {self.favorite_vk_id}, {self.first_last_name}, {self.link}, {self.photos}, {self.id_user}"


def create_tables(ENGINE):
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)
