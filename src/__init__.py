from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db = SQLAlchemy()
app = Flask("Api For Kuantaz")

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:root@localhost:5432/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
