from base import Base
from sqlalchemy import create_engine
from user import User
from category import Category
from item import Item


engine = create_engine('sqlite:///testingcatalog.db')
Base.metadata.create_all(engine)
