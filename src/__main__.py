from src import app, db
from flask_migrate import Migrate

from . import institution as inst
from . import project
from . import user

inst.build(app, inst.InstitutionService(db), inst.InstitutionMapper())
project.build(app, project.ProjectService(db), project.ProjectMapper())
user.build(app, user.UserService(db), user.UserMapper())

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
# TODO: Add Relations https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
# TODO: Add Dates ✅✅
#   https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
#   https://docs.sqlalchemy.org/en/14/core/defaults.html
# TODO: Read Specifications
# TODO: Add Swagger
# TODO: Add UnitTest
# TODO: Docker
# TODO: Create Readme
#   docker-version
#   python-version
