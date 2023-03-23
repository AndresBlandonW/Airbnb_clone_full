#!/usr/bin/python3
"""More Project Classes"""
from os import getenv
from sqlalchemy import Column, ForeignKey, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Class City that unheriths"""
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'cities'
        name = Column(String(128),
                      nullable=False)
        state_id = Column(String(60),
                          ForeignKey('states.id'),
                          nullable=False)
        places = relationship("Place",
                              backref="cities",
                              cascade="all, delete-orphan")
    else:
        state_id = ""
        name = ""
    
    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)