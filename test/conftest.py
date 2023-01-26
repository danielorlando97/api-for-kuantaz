import pytest
from flask import Flask
from flask_migrate import Migrate

from src import institution as inst
from src import project
from src import user
from src import db


from src.institution.model import InstitutionModel
import unit.institution_model_test as int_data

from src.project.model import ProjectModel
import unit.project_model_test as project_data

from src.user.model import UserModel
import unit.user_model_test as user_data


@pytest.fixture(scope='session')
def test_client():

    app = Flask("Api For Kuantaz")

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:root@localhost:5432/flask-test"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    inst.build(app, inst.InstitutionService(db), inst.InstitutionMapper())
    project.build(app, project.ProjectService(db), project.ProjectMapper())
    user.build(app, user.UserService(db), user.UserMapper())

    db.init_app(app)
    migrate = Migrate(app, db)

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            db.create_all()  # we should careful because all models has a relationship with a specific SQLAlchemy instance
            yield testing_client  # this is where the testing happens!

            db.session.remove()
            db.drop_all()


@pytest.fixture(scope='session')
def new_institution():
    def f():
        return InstitutionModel(int_data.name, int_data.description, int_data.direction)
    return f


@pytest.fixture(scope='session')
def new_project():
    return ProjectModel(
        name=project_data.name,
        description=project_data.description,
        start_date=project_data.start_date,
        end_date=project_data.end_date,
        main_user_id=-1,
        institution_id=-1
    )


@pytest.fixture(scope='session')
def new_user():
    return UserModel(
        name=user_data.name,
        last_name=user_data.last_name,
        rut=user_data.rut,
        office=user_data.office,
        birthday=user_data.birthday,
        age=-1
    )
