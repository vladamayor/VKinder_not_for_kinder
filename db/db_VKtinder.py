from db_VKtinder_models import create_tables, User, Candidat, Favorit
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, find_dotenv
from pprint import pprint

load_dotenv(find_dotenv())

DSN = f'postgresql://{os.getenv("LOGIN")}:{os.getenv("PASSWORD")}@' \
      f'{os.getenv("SERVER")}:{os.getenv("PORT")}/{os.getenv("DB_NAME")}'
engine = sqlalchemy.create_engine(DSN)

# create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


# Добавление ID user в базу
def adding_data_user(data):
    session.add(User(user_vk_id=data))
    session.commit()
    session.close()


# Добавляет даныые candidates в базу.
# (id кандидата, тья и фамилию, ссылку на страничку кандидата, фото, id user)
def adding_data_candidates(candidate_id, first_last_name, link, photos, user):
    session.add(Candidat(candidate_vk_id=candidate_id, first_last_name=first_last_name,
                         link=link, photos=photos, id_user=user))
    session.commit()
    session.close()


# Добавляет даныые в базу favorites.
# (id кандидата, тья и фамилию, ссылку на страничку кандидата, фото, id user)
def adding_data_favorites(favorite_vk_id, first_last_name, link, photos, user):
    session.add(Favorit(favorite_vk_id=favorite_vk_id, first_last_name=first_last_name,
                        link=link, photos=photos, id_user=user))
    session.commit()
    session.close()


# Выдает по одному кандидатов.
def issues_candidate(user_id):
    # Поиск ID в базе по его id в VK. Принимает на вход id VK, на выходе id в базе(Целое число)
    res = session.query(User.id).filter(User.user_vk_id == user_id).all()
    ress = res[0][0]
    # Выдает по одному кандидатов.
    for result in session.query(Candidat).filter(Candidat.id_user == ress).all():
        return result


def issues_favorite(user_id):
    # Поиск ID в базе по его id в VK. Принимает на вход id VK, на выходе id в базе(Целое число)
    res = session.query(User.id).filter(User.user_vk_id == user_id).all()
    ress = res[0][0]
    # Выдает по одному из избранных.
    for result in session.query(Favorit).filter(Favorit.id_user == ress).all():
        return result

# Удаление кандидата из таблицы candidates
def deleted_candidate(candidate_id):
    session.query(Candidat).filter(Candidat.candidate_vk_id == candidate_id).delete()
    session.commit()
    session.close()


def deleted_favorite(favorite_id):
    session.query(Favorit).filter(Favorit.favorite_vk_id == favorite_id).delete()
    session.commit()
    session.close()
