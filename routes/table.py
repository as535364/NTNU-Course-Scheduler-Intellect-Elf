from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import literal
from share.db import db
from model import Course

table_bp = Blueprint('table_bp', __name__, static_folder='static')


@table_bp.route('/', methods=['GET', 'POST'])
def table():
    # get all courses data
    courses = Course.query.all()
    dept_name_code = {}
    for course in courses:
        dept_name_code[course.dept_code] = course.department

    return render_template('table.html', values=courses, db_dept=dept_name_code)
# return redirect(url_for("login"))


@table_bp.route('/search', methods=['GET', 'POST'])
def search_course():
    # 拿 department 的代碼和 department
    courses = Course.query.all()
    dept_name_code = {}
    for course in courses:
        dept_name_code[course.dept_code] = course.department

    if request.method == 'POST':
        # 輸入搜尋
        print(request.form)

        # 搜尋課程名稱
        # 搜尋老師
        dept_code = request.values['dept'] if request.values['dept'] != '開課系所' else None
        condition = request.values['condition']

        course_searched = []
        if dept_code and condition != '':
            course_searched.extend(Course.query.filter_by(course_code=condition, dept_code=dept_code).all())
            course_searched.extend(Course.query.filter_by(course_name=condition, dept_code=dept_code).all())
            course_searched.extend(Course.query.filter_by(instructor=condition, dept_code=dept_code).all())
        elif not dept_code and condition != '':
            course_searched.extend(Course.query.filter_by(course_code=condition).all())
            course_searched.extend(Course.query.filter_by(course_name=condition).all())
            course_searched.extend(Course.query.filter_by(instructor=condition).all())
        elif dept_code and condition == '':
            course_searched.extend(Course.query.filter_by(dept_code=dept_code).all())
        course_searched = list(course_searched)
        print(course_searched)



        return render_template('table.html', course_searched=course_searched, db_dept=dept_name_code, condi=condition, dept_selected={'code': dept_code, 'name': dept_name_code[dept_code]})
    else:
        return render_template('table.html', values=course, db_dept=dept_name_code)



def get_dept():
    tdb_dept = db.session.query(Course.department).distinct()
    tdb_dept_code = db.session.query(Course.dept_code).distinct()
    db_dept = list()
    db_dept_code = list()

    for a in tdb_dept.all():
        s = str(a)
        db_dept.append(s[2:-3])
    for b in tdb_dept_code.all():
        s = str(b)
        db_dept_code.append(s[2:-3])
    dept_dic = dict(zip(db_dept_code,db_dept))
    # for key in dept_dic:
    #     print(key, dept_dic[key])
    return db_dept,db_dept_code,dept_dic
