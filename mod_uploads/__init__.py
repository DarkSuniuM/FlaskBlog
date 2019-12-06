from flask import Blueprint


uploads = Blueprint('uploads', __name__)


from . import models