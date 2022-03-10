from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os
load_dotenv()


db_url = os.getenv('DB_URI')

engine = create_engine(db_url, pool_size=100, echo=False)


# session_factory = sessionmaker(bind=engine)
Session = scoped_session(sessionmaker())

def init_session():
    Session.configure(bind=engine)
    from models import (Base)
    Base.metadata.create_all(bind=engine)
    