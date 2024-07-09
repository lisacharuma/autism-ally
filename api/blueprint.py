"""Use blueprint"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api')

from .users import *
from .resources import *
from .posts import *
from success_stories import *
