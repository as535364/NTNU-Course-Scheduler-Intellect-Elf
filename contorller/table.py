from flask import Blueprint, render_template, request, redirect, url_for

table = Blueprint('table', __name__, static_folder='static')


@table.route('/show')
def show():
    return render_template('table.html')
