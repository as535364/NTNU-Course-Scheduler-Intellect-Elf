from flask import Blueprint, render_template, request, redirect, url_for

account = Blueprint('account', __name__)


@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print(request.form)
        return redirect(url_for('account.login'))


@account.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        print(request.form)
        return redirect((url_for('index')))
