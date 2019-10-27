from flask import session
from . import admin


@admin.route('/')
def index():
    return "Hello from admin Index"


@admin.route('/login/')
def login():
    session['name'] = 'Alireza'
    # session.clear()
    # print(session.get('name'))
    print(session)
    return "1"
