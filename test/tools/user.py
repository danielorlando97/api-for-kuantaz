

from datetime import datetime

from src.user.model import UserModel

name = 'Tomas'
last_name = "Alasdos"
rut = '123456789'
birthday = datetime.now()
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
