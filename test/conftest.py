import pytest
from flask import Flask
from flask_migrate import Migrate

from src import institution as inst
from src import project
from src import user
from src import db


from dotenv import load_dotenv
from os import environ

load_dotenv()


@pytest.fixture(scope='session')
def test_client():

    app = Flask("Api For Kuantaz")

    db_type = environ.get("DATABASE_TYPE")
    db_user = environ.get("DATABASE_USER")
    db_pass_ = environ.get("DATABASE_PASS")
    db_host = environ.get("DATABASE_HOST")
    db_port = environ.get("DATABASE_PORT")
    db_name = environ.get("DATABASE_NAME_TEST")

    app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_type}://{db_user}:{db_pass_}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    inst_service = inst.InstitutionService(db)
    inst.build(app, inst_service, inst.InstitutionMapper())

    user_service = user.UserService(db)
    user.build(app, user_service, user.UserMapper())

    project.build(app, project.ProjectService(
        db, user_service, inst_service), project.ProjectMapper())

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.test_client() as testing_client:
        with app.app_context():
            # we should careful because all models has a
            # relationship with a specific SQLAlchemy instance
            db.create_all()
            yield testing_client

            db.session.remove()
            db.drop_all()
