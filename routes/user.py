import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from share.db import db
from share.login import login_required, admin_required
from model import User

user_bp = Blueprint('user_bp', __name__)


def user_form_validation(email, password, repeat_password, username=None):
    error = False
    if username is not None and not re.match(r"^\w{1,12}$", username):
        flash('帳號未輸入或是格式錯誤', 'error')
        error = True
        if User.query.filter_by(email=email).first():
            flash('帳號與其他帳號重複', 'error')
            error = True

    if email is not None:
        if not re.match(r".+@.+\..+", email):
            flash('Email 未輸入或是格式錯誤', 'error')
            error = True

    if (password is not None or repeat_password is not None) and \
            (not re.match(r"^.{1,30}$", password) or not re.match(r"^.{1,30}$", repeat_password)):
        flash('密碼以及重複密碼未輸入或是格式錯誤', 'error')
        error = True
        if password != repeat_password:
            flash('密碼以及重複密碼不一致', 'error')
            error = True

    return error


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
        if username == '' or password == '':
            flash('請輸入帳號密碼', 'error')
            error = True

        query_user_by_username = User.query.filter_by(username=username).first()
        if not error and query_user_by_username and password == query_user_by_username.password:
            flash('登入成功', 'success')
            is_login = True
        else:
            flash('帳號不存在或是帳號密碼錯誤', 'error')
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
        error = user_form_validation(data.get('email'), data.get('password'),
                                     data.get('repeatPassword'), data.get('username'))

        if User.query.filter_by(username=data.get('username')).first():
            flash('帳號與其他帳號重複', 'error')
            error = True

        # redirect
        dept_name = data.get('dept') if data.get('dept') else ''
        grade = data.get('grade') if data.get('grade') else 0
        if not error:
            user = User(username=data.get('username'), email=data.get('email'), password=data.get('password'),
                        dept_name=dept_name, grade=grade)
            db.session.add(user)
            db.session.commit()
            flash('註冊成功', 'success')
            return redirect((url_for('user_bp.login')))
        else:
            return render_template('register.html'), 400


@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        user = User.query.filter_by(username=session['username']).first()
        return render_template('profile.html', user=user)
    else:
        user = User.query.filter_by(username=session['username']).first()
        data = request.form
        email = data.get('email') if data.get('email') != '' else None
        password = data.get('password') if data.get('password') != '' else None
        repeat_password = data.get('repeatPassword') if data.get('repeatPassword') != '' else None

        error = user_form_validation(email, password, repeat_password)

        if not error:
            user.email = data.get('email') if data.get('email') else user.email
            user.password = data.get('password') if data.get('password') else user.password
            user.dept_name = data.get('dept') if data.get('dept') else user.dept_name
            user.grade = data.get('grade') if data.get('grade') else user.grade
            db.session.commit()
            flash('更新資料完成', 'success')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('user_bp.profile')), 400


@user_bp.route('/test/user')
@login_required
def test_user(user):
    return render_template('test.html', user=user)


@user_bp.route('/test/admin')
@admin_required
def test_admin(user):
    return render_template('test.html', user=user)
