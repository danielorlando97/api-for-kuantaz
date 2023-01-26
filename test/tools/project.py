

from datetime import datetime

from src.project.model import ProjectModel

name = 'IA'
description = 'A project'
start_date = datetime.now()
end_date = datetime.now()


def create(user_id=-1, inst_id=-1):
    return ProjectModel(
        name,
        description,
        start_date,
        end_date,
        user_id,
        inst_id
    )
