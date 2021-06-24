from flask import Blueprint, render_template, request, redirect, url_for, flash
from share.login import login_required
from sqlalchemy.sql import func
from share.db import db
from model import Course,Evaluation

table_bp = Blueprint('table_bp', __name__, static_folder='static')



def get_credits(user):

    credit = [0, 0, 0]
    for course in user.courses:
        credit[0] += course.credits
        if user.dept_name != '' and course.department.find(user.dept_name) != -1:
            credit[1] += course.credits
        elif course.dept_code == 'GU':
            credit[2] += course.credits
    return credit

def spilt_time(s):
    hole_time = []
    dic = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, 'A': 11, 'B': 12, 'C': 13, 'D': 14 }
    a = str(s).split(',')
    # 分兩段
    for b in a:
        t = str(b).split(' ')
        day = dic[t[0]]
        if t[1].find('-') != -1:
            time = t[1].split('-')
            start = dic[time[0]] if time[0].isalpha() else time[0]
            end = dic[time[1]] if time[1].isalpha() else time[1]
        else:
            start = dic[t[1]] if t[1].isalpha() else t[1]
            end = dic[t[1]] if t[1].isalpha() else t[1]
        hole_time.append([day, start, end])

    return hole_time


def parse_course_time(courses):
    table = []
    for j in range(6):
        table.append([])
    for j in range(6):
        for i in range(15):
            table[j].append([])

    for course in courses:
        # 有兩筆時間要處理
        hole_time = spilt_time(course.time)
        for time in hole_time:
            for i in range(int(time[1]), int(time[2]) + 1):
                table[time[0]][i].append(course)

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
    allcourses = Course.query.limit(100).all()

    table = parse_course_time(user_course)

    tmp = Course.query.filter(Course.department.contains(user.dept_name)).first()
    user_dept = tmp.dept_code

    return render_template('table.html', db_dept=dept_name_code, course_searched=allcourses, user_course=user_course, credit=credit, table=table, user_dept=user_dept, change_color = None, checked = None )



@table_bp.route('/add', methods=['POST'])
@login_required
def add_course(user):
    user_course = user.courses
    courses, dept_name_code = get_all_courses_code()

    tmp = Course.query.filter(Course.department.contains(user.dept_name)).first()
    user_dept = tmp.dept_code
    if request.method == 'POST':
        course_to_be_add = Course.query.filter_by(cid=request.form.get('cid')).first()
        if course_to_be_add not in user.courses:
            user.courses.append(course_to_be_add)
            db.session.commit()
            # print(course_to_be_add.course_name)
        credit = get_credits(user)
        table = parse_course_time(user_course)


        return render_template('table.html', db_dept=dept_name_code, user_course=user_course, credit=credit, table=table, user_dept=user_dept, change_color = None, sortchecked = None)


@table_bp.route('/remove', methods=['POST'])
@login_required
def remove_course(user):
    user_course = user.courses
    courses, dept_name_code = get_all_courses_code()
    if request.method == 'POST':
        # print(request.form.get('cid'))
        course_to_be_remove = Course.query.filter_by(cid=request.form.get('cid')).first()
        if course_to_be_remove in user.courses:
            user.courses.remove(course_to_be_remove)
            db.session.commit()
            # print(course_to_be_remove.course_name)
        credit = get_credits(user)
        table = parse_course_time(user_course)

        tmp = Course.query.filter(Course.department.contains(user.dept_name)).first()
        user_dept = tmp.dept_code
        return render_template('table.html', db_dept=dept_name_code, user_course=user_course, credit=credit, table=table, user_dept=user_dept , change_color = None, sortchecked = None)


@table_bp.route('/search', methods=['POST'])
@login_required
def search_course(user):
    # 拿 department 的代碼和 department
    credit = get_credits(user)
    courses, dept_name_code = get_all_courses_code()
    user_course = user.courses
    table = parse_course_time(user_course)
    if request.method == 'POST':

        dept_code = request.values['dept'] if request.values['dept'] != '開課系所' else None
        condition = request.values['condition']
        course_searched = []
        if dept_code and condition != '':
            course_searched.extend(Course.query.filter(Course.course_code.contains(condition)).filter_by(dept_code=dept_code).all())
            course_searched.extend(Course.query.filter(Course.serial_no.contains(condition)).filter_by(dept_code=dept_code).all())
            course_searched.extend(Course.query.filter(Course.course_name.contains(condition)).filter_by(dept_code=dept_code).all())
            course_searched.extend(Course.query.filter(Course.instructor.contains(condition)).filter_by(dept_code=dept_code).all())
        elif not dept_code and condition != '':
            course_searched.extend(Course.query.filter(Course.course_code.contains(condition)).all())
            course_searched.extend(Course.query.filter(Course.serial_no.contains(condition)).all())
            course_searched.extend(Course.query.filter(Course.course_name.contains(condition)).all())
            course_searched.extend(Course.query.filter(Course.instructor.contains(condition)).all())
        elif dept_code and condition == '':
            course_searched.extend(Course.query.filter_by(dept_code=dept_code).all())
        elif not dept_code and condition == '':
            course_searched = Course.query.all()
        course_searched = list(course_searched)
        # print(request.form['check-sort'])

        sort_course = []
        for course in course_searched:
            if request.form['check-sort'] == '1':
                avg_cool = Evaluation.query.with_entities(func.avg(Evaluation.cool)).filter(
                    Evaluation.course_id == course.cid).first()
                for b in avg_cool:
                    sort_course.append([course, b]) if( b is not None ) else sort_course.append([course, 0])
            elif request.form['check-sort'] == '2':
                avg_sweetness = Evaluation.query.with_entities(func.avg(Evaluation.sweetness)).filter(
                    Evaluation.course_id == course.cid).first()
                for b in avg_sweetness:
                    sort_course.append([course, b]) if (b is not None) else sort_course.append([course, 0])
            elif request.form['check-sort'] == '3':
                avg_gain = Evaluation.query.with_entities(func.avg(Evaluation.gain)).filter(
                    Evaluation.course_id == course.cid).first()
                for b in avg_gain:
                    sort_course.append([course, b]) if (b is not None) else sort_course.append([course, 0])

        # for course in sort_course:
        #     print( course )
        s_course = sorted(sort_course, key=lambda s: s[1], reverse = True)
        sort_course_searched = []
        for course in (s_course):
            sort_course_searched.append(course[0])
        # print(sort_course_searched)
        tmp = Course.query.filter(Course.department.contains(user.dept_name)).first()
        user_dept = tmp.dept_code
        return render_template('table.html',user_dept=user_dept, course_searched=sort_course_searched, db_dept=dept_name_code, condi=condition,
                               dept_selected=dept_name_code.get(dept_code), user_course=user_course, credit=credit, table=table, change_color = None, sortchecked = request.form['check-sort'])


@table_bp.route('/get_table', methods=['GET'])
@login_required
def get_table_course(user):
    credit = get_credits(user)
    courses, dept_name_code = get_all_courses_code()
    user_course = user.courses
    table = parse_course_time(user_course)
    tmp = Course.query.filter(Course.department.contains(user.dept_name)).first()
    user_dept = tmp.dept_code

    if request.method == 'GET':
    # 選課志願
        # print(request.args.get('day'))
        time = request.args.get('day')
        t = time.split('-')
        # print(t[0], t[1])
        user_course = table[int(t[0])-1][int(t[1])]

        tmp = [int(t[0]), int(t[1])]
        color_block = []
        color_block.append(tmp)
        # print( color_block )
    # 搜尋 --> 晚點做

    return render_template('table.html', db_dept=dept_name_code, user_course=user_course, credit=credit, table=table, user_dept=user_dept, change_color = color_block, sortchecked = None )

