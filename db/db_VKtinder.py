from db.db_VKtinder_models import create_tables, User, Candidat, Favorit
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DSN = (
    f'postgresql://{os.getenv("LOGIN")}:{os.getenv("PASSWORD")}@'
    f'{os.getenv("SERVER")}:{os.getenv("PORT")}/{os.getenv("DB_NAME")}'
)
ENGINE = sqlalchemy.create_engine(DSN)

create_tables(ENGINE)

Session = sessionmaker(bind=ENGINE)
SESSION = Session()


def adding_data_user(data):
    result = SESSION.query(User.user_vk_id).all()
    list_id_vk = []
    for item in result:
        list_id_vk.append(item[0])
    if data not in list_id_vk:
        SESSION.add(User(user_vk_id=data))
    else:
        pass
    SESSION.commit()
    SESSION.close()


def adding_data_candidates(candidate_id, first_last_name, link, user_id):
    res = SESSION.query(User.id).filter(User.user_vk_id == user_id).all()
    ress = res[0][0]
    SESSION.add(
        Candidat(
            candidate_vk_id=candidate_id,
            first_last_name=first_last_name,
            link=link,
            id_user=ress,
        )
    )
    SESSION.commit()
    SESSION.close()



def adding_data_favorites(favorite_vk_id, first_last_name, link, user_id):
    res = SESSION.query(User.id).filter(User.user_vk_id == user_id).all()
    ress = res[0][0]
    SESSION.add(
        Favorit(
            favorite_vk_id=favorite_vk_id,
            first_last_name=first_last_name,
            link=link,
            id_user=ress,
        )
    )
    SESSION.commit()
    SESSION.close()



def issues_candidate(user_id):
    res = SESSION.query(User.id).filter(User.user_vk_id == user_id).all()
    ress = res[0][0]
    result = (
        SESSION.query(Candidat.candidate_vk_id, Candidat.first_last_name, Candidat.link)
        .order_by(Candidat.id)
        .filter(Candidat.id_user == ress)
        .first()
    )
    print(result)
    return result

def issues_id_candidate(user_id):
    res = SESSION.query(User.id).filter(User.user_vk_id == user_id).all()
    ress = res[0][0]
    result = (
        SESSION.query(Candidat.candidate_vk_id)
        .order_by(Candidat.id)
        .filter(Candidat.id_user == ress)
        .first()
    )
    return result


def issues_favorite(user_id):
    res = SESSION.query(User.id).filter(User.user_vk_id == user_id).all()
    ress = res[0][0]
    result = (
        SESSION.query(Favorit.first_last_name, Favorit.link)
        .filter(Favorit.id_user == ress)
        .all()
    )
    return result



def deleted_candidate(candidate_id):
    SESSION.query(Candidat).filter(Candidat.candidate_vk_id == candidate_id).delete()
    SESSION.commit()
    SESSION.close()


def deleted_candidate_all(user_id):
    res = SESSION.query(User.id).filter(User.user_vk_id == user_id).all()
    ress = res[0][0]
    SESSION.query(Candidat).filter(Candidat.id_user == ress).delete()
    SESSION.commit()
    SESSION.close()


def deleted_favorite(favorite_id):
    SESSION.query(Favorit).filter(Favorit.favorite_vk_id == favorite_id).delete()
    SESSION.commit()
    SESSION.close()
