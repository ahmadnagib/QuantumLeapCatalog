from models import Base
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from user import User


class Category(Base):
    __tablename__ = 'category'

    # convert data into a format that allows it to
    # be shared later as json
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user': self.user.name,
        }

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    description = Column(String(800), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    created = Column(DateTime, default=func.now(), nullable=False)
    updated = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False)
