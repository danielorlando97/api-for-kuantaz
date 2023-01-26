from src.project.model import ProjectModel

name = 'IA'
description = 'A project'
start_date = "1997-04-01T00:00:00"
end_date = "1997-05-01T00:00:00"


def create(user_id=None, inst_id=None):
    return ProjectModel(
        name,
        description,
        start_date,
        end_date,
        user_id,
        inst_id
    )
