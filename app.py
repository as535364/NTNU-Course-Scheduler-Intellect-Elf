from flask import Flask
from account.api import account

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello index"


app.register_blueprint(account, url_prefix='/')
