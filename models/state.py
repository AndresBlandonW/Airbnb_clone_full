#!/usr/bin/python3
"""More Project Classes"""
from os import getenv
from sqlalchemy import Column, String
import models
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """Class State that unheriths"""
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128),
                      nullable=False)
    else:
        name = ""

    @property
    def cities(self):
        """fs getter attribute that returns City instances"""
        values_city = models.storage.all("City").values()
        list_city = []
        for city in values_city:
            if city.state_id == self.id:
                list_city.append(city)
        return list_city
