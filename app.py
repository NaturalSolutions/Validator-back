# -----MODELS AND CONFIG---------

from flask import Flask, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.cfg')

from models import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# -----ROUTES---------
from routes import *
app.register_blueprint(routes)





if __name__ == "__main__":
    app.run(host='0.0.0.0')
    manager.run()
