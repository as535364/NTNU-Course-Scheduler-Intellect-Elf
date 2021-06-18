from flask import Flask, render_template
from account.api import account
from table.api import table

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(account, url_prefix='/')
app.register_blueprint(table, url_prefix='/')
