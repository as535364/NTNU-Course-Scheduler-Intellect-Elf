from flask import Blueprint, render_template, request, redirect, url_for, flash
from share.login import login_required
from collections import defaultdict
from share.db import db
from model import Course

table_bp = Blueprint('table_bp', __name__, static_folder='static')


def get_credits(user):

    credit = [0, 0, 0]
    for course in user.courses:
        credit[0] += course.credits
        if user.dept_name is not None and course.department == user.dept_name:
            credit[1] += course.credits
        elif course.dept_code == 'GU':
            credit[2] += course.credits
    return credit

def spilt_time(s):
    t = str(s).split(' ')
    dic = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, 'A': 11, 'B': 12, 'C': 13, 'D': 14 }
    day = dic[t[0]]
    time = t[1].split('-')
    print(time)
    start = dic[time[0]] if time[0].isalpha() else time[0]
    end = dic[time[1]] if time[1].isalpha() else time[1]

    return day, start, end


def parse_course_time(courses):
    table = []
    for j in range(6):
        table.append([])
    for j in range(6):
        for i in range(15):
            table[j].append([])

    for course in courses:
        day, start, end = spilt_time(course.time)
        for i in range( int(start), int(end)+1 ):
            # print(i)
            table[day][i].append(course)
    #     print(int(time[0]),int(time[1]))
    # print(table)
    return table


def get_course_table(user):
    credit = [0, 0, 0]
    for course in user.courses:
        credit[0] += course.credits
        if user.dept_name is not None and course.department == user.dept_name:
            credit[1] += course.credits
        elif course.dept_code == 'GU':
            credit[2] += course.credits
    return credit


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
    credit = get_credits(user)
    courses, dept_name_code = get_all_courses_code()
    user_course = user.courses
    # parse_course_time(user_course)

    table = parse_course_time(user_course)
    user_dept = user.dept_name

    return render_template('table.html', db_dept=dept_name_code, user_course=user_course, credit=credit, table=table, user_dept=user_dept, change_color = None )


# return redirect(url_for("login"))


@table_bp.route('/add', methods=['POST'])
@login_required
def add_course(user):
    user_course = user.courses
    courses, dept_name_code = get_all_courses_code()
    if request.method == 'POST':
        course_to_be_add = Course.query.filter_by(cid=request.form.get('cid')).first()
        if course_to_be_add not in user.courses:
            user.courses.append(course_to_be_add)
            db.session.commit()
            print(course_to_be_add.course_name)
        credit = get_credits(user)
        table = parse_course_time(user_course)
        user_dept = user.dept_name
        return render_template('table.html', db_dept=dept_name_code, user_course=user_course, credit=credit, table=table, user_dept=user_dept, change_color = None)


@table_bp.route('/remove', methods=['POST'])
@login_required
def remove_course(user):
    user_course = user.courses
    courses, dept_name_code = get_all_courses_code()
    if request.method == 'POST':
        print(request.form.get('cid'))
        course_to_be_remove = Course.query.filter_by(cid=request.form.get('cid')).first()
        if course_to_be_remove in user.courses:
            user.courses.remove(course_to_be_remove)
            db.session.commit()
            print(course_to_be_remove.course_name)
        credit = get_credits(user)
        table = parse_course_time(user_course)
        user_dept = user.dept_name
        return render_template('table.html', db_dept=dept_name_code, user_course=user_course, credit=credit, table=table, user_dept=user_dept , change_color = None)


@table_bp.route('/search', methods=['POST'])
@login_required
def search_course(user):
    # 拿 department 的代碼和 department
    credit = get_credits(user)
    courses, dept_name_code = get_all_courses_code()
    user_course = user.courses
    table = parse_course_time(user_course)
    user_dept = user.dept_name
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
        return render_template('table.html', course_searched=course_searched, db_dept=dept_name_code, condi=condition,
                               dept_selected=dept_name_code.get(dept_code), user_course=user_course, credit=credit, table=table, user_dept=user_dept, change_color = None)


@table_bp.route('/get_table', methods=['GET'])
@login_required
def get_table_course(user):
    credit = get_credits(user)
    courses, dept_name_code = get_all_courses_code()
    user_course = user.courses
    table = parse_course_time(user_course)
    user_dept = user.dept_name
    if request.method == 'GET':
    # 選課志願
        # print(request.args.get('day'))
        time = request.args.get('day')
        print(time)
        t = time.split('-')
        print(t[0], t[1])
        user_course = table[int(t[0])-1][int(t[1])]
        print(user_course)

        tmp = [int(t[0]), int(t[1])]
        color_block = []
        color_block.append(tmp)
        print( color_block )
    # 搜尋 --> 晚點做

    return render_template('table.html', db_dept=dept_name_code, user_course=user_course, credit=credit, table=table, user_dept=user_dept, change_color = color_block )

