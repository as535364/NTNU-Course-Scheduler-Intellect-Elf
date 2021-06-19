from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from contorller.user import user
from contorller.table import table

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')



app.register_blueprint(user, url_prefix='/')
app.register_blueprint(table, url_prefix='/')
