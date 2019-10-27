from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin/')

from .views import index
