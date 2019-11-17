from flask import Flask

app = Flask(__name__)

from secret_santa.controller import participant_controller
from secret_santa.controller import secret_santa_controller

from secret_santa.database import db_session, init_db



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
