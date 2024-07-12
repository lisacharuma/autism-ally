"""Use blueprint"""

from flask import Blueprint

api_views = Blueprint('api_views', __name__)

from .users import *
from .resources import *
from .posts import *
from success_stories import *
