from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
from os import environ

db = SQLAlchemy()
app = Flask("Api For Kuantaz")

load_dotenv()
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:root@localhost:5432/flask"

db_type = environ.get("DATABASE_TYPE")
user = environ.get("DATABASE_USER")
pass_ = environ.get("DATABASE_PASS")
host = environ.get("DATABASE_HOST")
port = environ.get("DATABASE_PORT")
name = environ.get("DATABASE_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_type}://{user}:{pass_}@{host}:{port}/{name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
