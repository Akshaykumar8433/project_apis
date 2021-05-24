from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(os.environ["dbuser"],os.environ["dbpass"],os.environ["dburl"],os.environ["dbport"],os.environ["database"]))
dbsession = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = dbsession.query_property()

def init_db():
    import modules.movies
    Base.metadata.create_all(bind=engine)

