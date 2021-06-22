from flask import Blueprint, render_template, request, redirect, url_for, flash
from share.db import db
from model import Course

table_bp = Blueprint('table_bp', __name__, static_folder='static')


@table_bp.route('/table', methods=['GET', 'POST'])
def table():
    # get all courses data
    course = Course.query.all()
    # for item in course:
    #     print(item.course_name)
    return render_template('table.html', values=course)
# return redirect(url_for("login"))


@table_bp.route('/table/search', methods=['GET', 'POST'])
def search_course():
    tex = []
    if request.method == 'POST':
        print(request.form)
        if request.form.get('condition') is not None:
            tex.append(request.values['condition'])

        tex.append(request.values.get('btnTypeTex'))
        # if request.form.get('btnDeptTex') != '開課系所':
        #     tex.append(request.values['btnDeptTex'])
        print(tex)

        return render_template('table.html')
    else:
        return render_template('table.html')
