from db_VKtinder_models import User, Candidates, Favorites


DSN = f'postgresql://{os.getenv("LOGIN")}:{os.getenv("PASSWORD")}@{os.getenv("SERVER")}:{os.getenv("PORT")}/{os.getenv("DB_NAME")}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()




def adding_data(session, data):
    ...

    session.add_all(resault)
    session.commit()