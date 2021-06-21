from flask import Blueprint, render_template, request, redirect, url_for

table_bp = Blueprint('table_bp', __name__, static_folder='static')


@table_bp.route('/show')
def show():
    return render_template('table.html')
