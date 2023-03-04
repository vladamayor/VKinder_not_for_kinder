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
    session.add(User(user_id=data))
    session.commit()
    session.close()


test_id = 1111111
# adding_data_user(test_id)

test_id1 = 2222222


# adding_data_user(test_id1)


# Добавляет даныые candidates в базу.
# (id кандидата, тья и фамилию, ссылку на страничку кандидата, фото, id user)
def adding_data_candidates(candidate_id, first_last_name, link, photos, user):
    session.add(Candidat(candidate_id=candidate_id, first_last_name=first_last_name,
                         link=link, photos=photos, id_user=user))
    session.commit()
    session.close()


test_can_id = 7849365
test_f_l_name = 'Майская Даздраперма'
test_link = 'https://vk.com/id7849365'
test_photos = 'https://sun1-85.userapi.com/impg/qJXqmpjIewHkB2_TtP8lKTmnh572_hkDoLCXgA/uhXitPz3oEg.jpg?size=750x926&quality=95&sign=2b22adf8e9901fd75f445123917f15ed&c_uniq_tag=clixN-h283e4NKP6-Ly57wLFkrEqefw9ssC176J829c&type=album, ' \
              'https://sun9-54.userapi.com/impg/YVOykrl63QfNyG20FUEH7WPSFXwYGbUpFIP22A/tF1WwSX_VgI.jpg?size=1280x1273&quality=95&sign=6bae4972ec0097cb7422f38e6c348c3a&c_uniq_tag=_G3Rkht8mtolXwt4q-H6LbXG0AfoFdyi12n7vXr--2k&type=album, ' \
              'https://sun1-47.userapi.com/impg/OYSCmxU7SVrrgunYwsEG0HSk23jQcc_pYWfijg/B7plNi883rw.jpg?size=886x1080&quality=96&sign=31e3e06cd433a6caff446c630439025e&c_uniq_tag=q2sR8eLMMRhMs1suMmLl2I1fHO7o0DGdK2p4qgpKDLk&type=album'
test_user = 1
# adding_data_candidates(test_can_id, test_f_l_name, test_link, test_photos, test_user)

test_can_id1 = 7849366
test_f_l_name1 = 'Полудурок Иван'
test_link1 = 'https://vk.com/id7849366'
test_photos1 = 'https://sun1-85.userapi.com/impg/qJXqmpjIewHkB2_TtP8lKTmnh572_hkDoLCXgA/uhXitPz3oEg.jpg?size=750x926&quality=95&sign=2b22adf8e9901fd75f445123917f15ed&c_uniq_tag=clixN-h283e4NKP6-Ly57wLFkrEqefw9ssC176J829c&type=album, ' \
               'https://sun9-54.userapi.com/impg/YVOykrl63QfNyG20FUEH7WPSFXwYGbUpFIP22A/tF1WwSX_VgI.jpg?size=1280x1273&quality=95&sign=6bae4972ec0097cb7422f38e6c348c3a&c_uniq_tag=_G3Rkht8mtolXwt4q-H6LbXG0AfoFdyi12n7vXr--2k&type=album, ' \
               'https://sun1-47.userapi.com/impg/OYSCmxU7SVrrgunYwsEG0HSk23jQcc_pYWfijg/B7plNi883rw.jpg?size=886x1080&quality=96&sign=31e3e06cd433a6caff446c630439025e&c_uniq_tag=q2sR8eLMMRhMs1suMmLl2I1fHO7o0DGdK2p4qgpKDLk&type=album'
test_user1 = 1


# adding_data_candidates(test_can_id1, test_f_l_name1, test_link1, test_photos1, test_user1)

# Добавляет даныые в базу favorites.
# (id кандидата, тья и фамилию, ссылку на страничку кандидата, фото, id user)
# def adding_data_favorites(favorite_id, first_last_name, link, photos, user):
#     session.add(Favorit(favorite_id=favorite_id, first_last_name=first_last_name,
#                         link=link, photos=photos, id_user=user))
#     session.commit()
#     session.close()

# Выдает по одному кандидатов.
def issues_candidate(user_id):
    # Поиск ID в базе по его id в VK. Принимает на вход id VK, на выходе id в базе(Целое число)
    res = session.query(User.id).filter(User.user_id == user_id).all()
    ress = res[0][0]
    # Выдает по одному кандидатов.
    for result in session.query(Candidat).filter(Candidat.id_user == ress).all():
        return result


# Удаление кандидата из таблицы candidates
def deleted_candidate(candidate_id):
    session.query(Candidat).filter(Candidat.candidate_id == candidate_id).delete()
    session.commit()
    session.close()


# print(issues_candidate(test_id))
for test in session.query(Candidat).all():
    print(test)
