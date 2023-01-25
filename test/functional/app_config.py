# from flask_testing import TestCase
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# from flask_migrate import Migrate

# from src import institution as inst
# from src import project
# from src import user


# class ApiTest(TestCase):

#     TESTING = True

#     def create_app(self):

#         self.db = SQLAlchemy()
#         app = Flask("Api For Kuantaz")

#         app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:root@localhost:5432/flask-test"
#         # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#         inst.build(app, inst.InstitutionService(
#             self.db), inst.InstitutionMapper())
#         project.build(app, project.ProjectService(
#             self.db), project.ProjectMapper())
#         user.build(app, user.UserService(self.db), user.UserMapper())

#         self.db.init_app(app)
#         return app

#     def setUp(self):
#         print("""


#         Holaaa


#         """)
#         self.db.create_all()

#     def tearDown(self):

#         self.db.session.remove()
#         self.db.drop_all()


# import pytest


# @pytest.fixture(scope='session')
# def test_client():


#     db.init_app(app)
#     migrate = Migrate(app, db)

#     # Create a test client using the Flask application configured for testing
#     with app.test_client() as testing_client:
#         # Establish an application context
#         with app.app_context():
#             db.create_all()
#             yield testing_client  # this is where the testing happens!
