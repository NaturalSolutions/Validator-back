from flask import Blueprint
routes = Blueprint('routes', __name__) #initialisation du blueprint avec l'argument 'routes' utilisé dans les decorateurs des def de routes.

from .pois import *
from .contributions import *
from .users import *
from .versions import *