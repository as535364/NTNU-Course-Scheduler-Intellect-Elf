from flask import Flask, render_template
from account.api import account

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(account, url_prefix='/')
