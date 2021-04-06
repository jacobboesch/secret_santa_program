from flask import Flask

app = Flask(__name__)

from secret_santa.controller import secret_santa_controller