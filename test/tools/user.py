

from datetime import datetime

from src.user.model import UserModel

name = 'Tomas'
last_name = "Alasdos"
rut = '123456789'
birthday = "1997-04-01T00:00:00"
office = 'developer'


def create():
    return UserModel(
        name,
        last_name,
        rut,
        birthday,
        office,
        age=-1
    )
