#!/usr/bin/python3
"""City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """a city obj

    Attributes:
        state_id (str): state id.
        name (str): name.
    """

    state_id = ""
    name = ""
