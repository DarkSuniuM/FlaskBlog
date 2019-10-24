from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Development


app = Flask(__name__)
app.config.from_object(Development)

db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Blog Home."

from mod_admin import admin

app.register_blueprint(admin)
