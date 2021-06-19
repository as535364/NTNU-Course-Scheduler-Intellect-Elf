from flask import Blueprint, render_template, request, redirect, url_for
# from model.user import User

user = Blueprint('user', __name__)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print(request.form)
        return redirect(url_for('account.login'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        print(request.form)
        return redirect((url_for('index')))
