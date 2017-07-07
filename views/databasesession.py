from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///testingcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()