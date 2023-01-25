import pytest
from flask import Flask
from flask_migrate import Migrate

from src import institution as inst
from src import project
from src import user
from src import db


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
