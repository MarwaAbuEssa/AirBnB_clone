#!/usr/bin/python3
"""Place class."""
from models.base_model import BaseModel


class Place(BaseModel):
    """a place obj.

    Attributes:
        city_id (str): city id.
        user_id (str): user id.
        name (str): name.
        description (str): description.
        number_rooms (int): num of rooms.
        number_bathrooms (int): num of bathrooms.
        max_guest (int): max  guests.
        price_by_night (int): price/night.
        latitude (float): latitude.
        longitude (float): longitude.
        amenity_ids (list): A list of Amenity ids.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
