from flask import Blueprint, render_template, request, redirect, url_for, flash
from share.login import login_required
from share.db import db
from model import Course

table_bp = Blueprint('table_bp', __name__, static_folder='static')


def print_user(user):
    print(user.username)


def get_all_courses_code():
    courses = Course.query.all()
    dept_name_code = {}
    for course in courses:
        dept_name_code[course.dept_code] = course.department
    return courses, dept_name_code


@table_bp.route('/', methods=['GET', 'POST'])
@login_required
def table(user):
    # get all courses data
    print_user(user)
    courses, dept_name_code = get_all_courses_code()
    user_course = user.courses

    return render_template('table.html', course =courses, db_dept=dept_name_code, user_course = user_course)
# return redirect(url_for("login"))


@table_bp.route('/add', methods=['POST'])
@login_required
def add_course(user):
    courses, dept_name_code = get_all_courses_code()
    if request.method == 'POST':
        course_to_be_add = Course.query.filter_by(cid=request.form.get('cid')).first()
        if course_to_be_add not in user.courses:
            user.courses.append(course_to_be_add)
            db.session.commit()
        print(course_to_be_add.course_name)
        return render_template('table.html', values=courses, db_dept=dept_name_code)


@table_bp.route('/remove', methods=['POST'])
@login_required
def remove_course(user):
    courses = Course.query.all()
    dept_name_code = {}
    for course in courses:
        dept_name_code[course.dept_code] = course.department
    if request.method == 'POST':
        course_to_be_remove = Course.query.filter_by(cid=request.form.get('cid')).first()
        user.courses.remove(course_to_be_remove)
        db.session.commit()
        print(course_to_be_remove.course_name)
        return render_template('table.html', values=courses, db_dept=dept_name_code )


@table_bp.route('/search', methods=['POST'])
def search_course():
    # 拿 department 的代碼和 department
    courses, dept_name_code = get_all_courses_code()

    if request.method == 'POST':
        # 輸入搜尋

        # 搜尋課程名稱
        # 搜尋老師
        dept_code = request.values['dept'] if request.values['dept'] != '開課系所' else None
        condition = request.values['condition']

        course_searched = []
        if dept_code and condition != '':
            course_searched.extend(Course.query.filter_by(course_code=condition, dept_code=dept_code).all())
            course_searched.extend(Course.query.filter_by(serial_no=condition, dept_code=dept_code).all())
            course_searched.extend(Course.query.filter_by(course_name=condition, dept_code=dept_code).all())
            course_searched.extend(Course.query.filter_by(instructor=condition, dept_code=dept_code).all())
        elif not dept_code and condition != '':
            course_searched.extend(Course.query.filter_by(course_code=condition).all())
            course_searched.extend(Course.query.filter_by(serial_no=condition).all())
            course_searched.extend(Course.query.filter_by(course_name=condition).all())
            course_searched.extend(Course.query.filter_by(instructor=condition).all())
        elif dept_code and condition == '':
            course_searched.extend(Course.query.filter_by(dept_code=dept_code).all())
        course_searched = list(course_searched)
        return render_template('table.html', course_searched=course_searched, db_dept=dept_name_code, condi=condition, dept_selected=dept_name_code.get(dept_code))
