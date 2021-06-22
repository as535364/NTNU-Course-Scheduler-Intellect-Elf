from flask import session, flash, redirect, url_for
from model import User
from functools import wraps


def is_login():
    return session.get('username')


def is_admin():
    return session.get('is_admin')


def login_required(func):
    """
    Required user to login
    Returns:
        - A wrapped function
        - 403 Not Logged In
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_login() is None:
            flash('請登入以使用功能', 'error')
            return redirect(url_for('user_bp.login')), 403
        else:
            user = User.query.filter_by(username=session['username']).first()
            kwargs['user'] = user
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """
    Required user to login
    Returns:
        - A wrapped function
        - 403 Not Logged In or Not admin
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_login() is None or not is_admin():
            flash('請以管理員身份登入以使用功能', 'error')
            return redirect(url_for('user_bp.login')), 403
        else:
            user = User.query.filter_by(username=session['username']).first()
            kwargs['user'] = user
        return func(*args, **kwargs)
    return wrapper
