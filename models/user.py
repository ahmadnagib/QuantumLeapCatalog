from models import Base
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    # convert data into a format that allows it to
    # be shared later as json
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
        }

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(400))
    created = Column(DateTime, default=func.now(), nullable=False)
    updated = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False)
