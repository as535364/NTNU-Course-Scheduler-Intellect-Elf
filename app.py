from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from routes.user import user_bp
from routes.table import table_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(user_bp, url_prefix='/')
app.register_blueprint(table_bp, url_prefix='/')
