from db_VKtinder_models import create_tables, User, Candidat, Favorit
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


DSN = f'postgresql://{os.getenv("LOGIN")}:{os.getenv("PASSWORD")}@' \
      f'{os.getenv("SERVER")}:{os.getenv("PORT")}/{os.getenv("DB_NAME")}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()



# Добавление ID user в базу
def adding_data_user(data):
    session.add_all(user_id=data)
    session.commit()
    session.close()



