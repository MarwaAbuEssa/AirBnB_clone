#!/usr/bin/python3
"""user class"""
from models.base_model import BaseModel


class User(BaseModel):
    """ a User object.

    Attributes:
        email (str): user email.
        password (str): password.
        first_name (str): first name.
        last_name (str): last name .
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
