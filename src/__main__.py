from src import app, db
from flask_migrate import Migrate
from flasgger import Swagger
from dotenv import load_dotenv
from os import environ

from . import institution as inst
from . import project
from . import user

load_dotenv()

inst_service = inst.InstitutionService(db)
inst.build(app, inst_service, inst.InstitutionMapper())

user_service = user.UserService(db)
user.build(app, user_service, user.UserMapper())

project.build(app, project.ProjectService(
    db, user_service, inst_service), project.ProjectMapper())


swagger = Swagger(app)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


app.run(
    host=environ.get('HOST', '127.0.0.1'),
    debug=environ.get("DEBUG_MODE", False),
    port=environ.get("PORT", 5000),
)
