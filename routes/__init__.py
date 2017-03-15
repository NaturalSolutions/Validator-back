from flask import Blueprint
routes = Blueprint('routes', __name__)

from .pois import *
from .contributions import *
from .users import *
from .versions import *