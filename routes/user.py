import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from share.db import db
from model import User

user_bp = Blueprint('user_bp', __name__)

# TODO login_required


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # validation
        data = request.form
        username = data.get('username')
        password = data.get('password')
        error = False
        if not username or not password:
            flash('請輸入帳號密碼', 'error')
            error = True

        query_user_by_username = User.query.filter_by(username=username).first()
        if not error and query_user_by_username and password == query_user_by_username.password:
            flash('登入成功', 'success')
            is_login = True
        else:
            flash('登入失敗', 'error')
            is_login = False

        # redirect
        if is_login:
            session['username'] = query_user_by_username.username
            session['is_admin'] = query_user_by_username.is_admin
            return redirect(url_for('index'))
        else:
            return redirect(url_for('user_bp.login')), 403


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # validation
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        repeat_password = data.get('repeatPassword')
        dept_name = data.get('dept_name') if data.get('dept_name') else ''
        grade = data.get('grade') if data.get('grade') else 0
        error = False
        if not re.match(r"^\w{1,12}$", username):
            flash('帳號未輸入或是格式錯誤', 'error')
            error = True
        if not re.match(r".+@.+\..+", email):
            flash('Email 未輸入或是格式錯誤', 'error')
            error = True
        if not password or not repeat_password or not re.match(r"^.{1,30}$", password) or \
                not re.match(r"^.{1,30}$", repeat_password):
            flash('密碼以及重複密碼未輸入或是格式錯誤', 'error')
            error = True
        if password != repeat_password:
            flash('密碼以及重複密碼不一致', 'error')
            error = True
        query_user_by_username = User.query.filter_by(username=username).first()
        query_user_by_email = User.query.filter_by(email=email).first()
        if query_user_by_email:
            flash('Email 與其他帳號重複', 'error')
            error = True
        if query_user_by_username:
            flash('帳號與其他帳號重複', 'error')
            error = True
        # redirect
        if not error:
            user = User(username=username, email=email, password=password, dept_name=dept_name, grade=grade)
            db.session.add(user)
            db.session.commit()
            flash('註冊成功', 'success')
            return redirect((url_for('user_bp.login')))
        else:
            return render_template('register.html'), 400
