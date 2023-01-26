from src.institution.model import InstitutionModel


name = 'Institution'
description = "A fine place"
direction = '32 C/ A and B'


def create():
    return InstitutionModel(name, description, direction)
