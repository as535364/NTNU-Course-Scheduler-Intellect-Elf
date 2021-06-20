from flask import Blueprint, render_template, request, redirect, url_for, flash
from share.db import db
from model import User

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.form
        username = data.get('username')
        password = data.get('password')
        error = False
        if not username:
            flash('請輸入帳號', 'error')
            error = True
        if not password:
            flash('請輸入密碼', 'error')
            error = True

        return redirect(url_for('account.login'))


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        repeat_password = data.get('repeatPassword')
        dept_name = data.get('dept_name') if data.get('dept_name') else ''
        grade = data.get('grade') if data.get('grade') else 0
        error = False
        if not username:
            flash('請輸入帳號', 'error')
            error = True
        if not email:
            flash('請輸入 Email', 'error')
            error = True
        if not password or not repeat_password:
            flash('請輸入密碼以及重複密碼', 'error')
            error = True
        if password != repeat_password:
            flash('密碼以及重複密碼不一致', 'error')
            error = True
        if not error:
            user = User(username=username, email=email, password=password, dept_name=dept_name, grade=grade)
            print(user)
            db.session.add(user)
            db.session.commit()
            return redirect((url_for('user_bp.login')))
        else:
            return render_template('register.html')
