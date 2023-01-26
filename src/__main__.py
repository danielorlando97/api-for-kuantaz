from src import app, db
from flask_migrate import Migrate
from flasgger import Swagger

from . import institution as inst
from . import project
from . import user

inst.build(app, inst.InstitutionService(db), inst.InstitutionMapper())
project.build(app, project.ProjectService(db), project.ProjectMapper())
user.build(app, user.UserService(db), user.UserMapper())


swagger = Swagger(app)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
app.run(debug=True)

# https://stackabuse.com/using-sqlalchemy-with-flask-and-postgresql/
# https://www.askpython.com/python-modules/flask/flask-postgresql
# https://stackoverflow.com/questions/11774265/how-do-you-access-the-query-string-in-flask-routes

# TODO: Validate inputs ✅✅
#   https://stackoverflow.com/questions/61644396/flask-how-to-make-validation-on-request-json-and-json-schema
#   https://stackoverflow.com/questions/57664997/how-to-return-400-bad-request-on-flask
# TODO: Add Relations ✅✅ https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
# TODO: Add Dates ✅✅
#   https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
#   https://docs.sqlalchemy.org/en/14/core/defaults.html
# TODO: Read Specifications ✅✅
# TODO: Add Swagger  ✅✅
#   https://flask-restplus.readthedocs.io/en/stable/quickstart.html
#   https://github.com/flasgger/flasgger
#   https://medium.com/analytics-vidhya/flasgger-an-api-playground-with-flask-and-swagger-ui-6b6806cf8884
# TODO: Add UnitTest
#   https://testdriven.io/blog/flask-pytest/
#   https://flask.palletsprojects.com/en/2.2.x/testing/
# TODO: Docker and Env
# TODO: Create Readme
#   docker-version
#   python-version
#   401 para los proyectos
#   sagger project
