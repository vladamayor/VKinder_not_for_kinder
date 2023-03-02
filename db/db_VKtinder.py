from db_VKtinder_models import User, Candidates, Favorites
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

DSN = f'postgresql://{os.getenv("LOGIN")}:{os.getenv("PASSWORD")}@' \
      f'{os.getenv("SERVER")}:{os.getenv("PORT")}/{os.getenv("DB_NAME")}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()




def adding_data(data):
    ...

    session.add_all(resault)
    session.commit()