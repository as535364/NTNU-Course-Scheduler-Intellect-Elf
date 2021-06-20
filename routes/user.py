from flask import Blueprint, render_template, request, redirect, url_for
from model import User

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print(request.form)
        return redirect(url_for('account.login'))


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        data = request.form
        now_user = User(email=data.get('email'), username=data.get('username'), password=data.get('password'), dept_name=data.get('dept_name'), grade=data.get('grade'))
        return redirect((url_for('index')))
