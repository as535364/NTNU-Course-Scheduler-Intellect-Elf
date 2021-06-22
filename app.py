from flask import Flask, render_template
from share.db import db
from routes.user import user_bp
from routes.table import table_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'Your Key'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


with app.app_context():
    db.create_all()

app.register_blueprint(user_bp, url_prefix='/')
app.register_blueprint(table_bp, url_prefix='/table')
