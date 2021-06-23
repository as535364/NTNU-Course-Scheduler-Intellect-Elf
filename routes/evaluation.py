from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.sql import func
from model import Evaluation, Course
from share.login import login_required, admin_required
from share.db import db


evaluation_bp = Blueprint('evaluation_bp', __name__)


@evaluation_bp.route('/view/<cid>', methods=['GET'])
def view(cid):
    if request.method == 'GET':
        #課程資訊
        course_data = Course.query.filter_by(cid=cid).first()
        serial_no = course_data.serial_no
        year = course_data.year
        term = course_data.term
        department = course_data.department
        course_name = course_data.course_name
        course_code = course_data.course_code
        restrict = course_data.restrict
        quota = course_data.quota
        authorize_quota = course_data.authorize_quota
        interschool_quota = course_data.interschool_quota
        instructor = course_data.instructor
        reg_sel = course_data.reg_sel
        credits = course_data.credits
        english = course_data.english
        time = course_data.time
        location = course_data.location
        note = course_data.note
        # 課程評分
        avg_sweetness = Evaluation.query.with_entities(func.avg(Evaluation.sweetness)).filter(Evaluation.course_id == cid).first()
        avg_cool = Evaluation.query.with_entities(func.avg(Evaluation.cool)).filter(Evaluation.course_id == cid).first()
        avg_gain = Evaluation.query.with_entities(func.avg(Evaluation.gain)).filter(Evaluation.course_id == cid).first()
        # 課程評價
        evaluation_data = Evaluation.query.filter_by(course_id=cid).all()
        return render_template('view_evaluation.html', evaluation_data=evaluation_data, sweetness=avg_sweetness[0], cool=avg_cool[0], gain=avg_gain[0],
                               serial_no=serial_no, term=term,
                               year=year, department=department, course_name=course_name, course_code=course_code,
                               restrict=restrict, quota=quota, authorize_quota=authorize_quota,
                               interschool_quota=interschool_quota, instructor=instructor, reg_sel=reg_sel,
                               credits=credits, english=english, time=time, location=location, note=note)


@evaluation_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add(user):
    if request.method == 'GET':
        checkdata = Evaluation.query.filter_by(username=user, course_id=1).first()
        error = False
        if checkdata:
            flash('已有評價紀錄，如欲編輯評價請點選 "編輯評價"', 'error')
            error = True
            return redirect(url_for('evaluation_bp.view'))
        else:
            return render_template('add_evaluation.html')
    else:
        data = request.form
        sweetness = data.get('sweet')
        cool = data.get('cool')
        gain = data.get('gain')
        description = data.get('description')
        error = False
        if not sweetness:
            flash('請選擇甜度', 'error')
            error = True
        if not cool:
            flash('請選擇涼度', 'error')
            error = True
        if not gain:
            flash('請選擇收穫', 'error')
            error = True
        if not description:
            flash('請輸入評價', 'error')
            error = True
        if not error:
            evaluation = Evaluation(username=user, course_id=1, sweetness=sweetness, cool=cool, gain=gain,
                                    description=description)
            db.session.add(evaluation)
            db.session.commit()
            flash('評價儲存成功', 'success')
            return redirect(url_for('evaluation_bp.view'))
        else:
            return redirect(url_for('evaluation_bp.add'))


@evaluation_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit(user):
    if request.method == 'GET':
        data = Evaluation.query.filter_by(username='40711014e', course_id=1).first()
        error = False
        if not data:
            flash('查無評價紀錄，如欲新增評價請點選 "新增評價"', 'error')
            error = True
            return redirect(url_for('evaluation_bp.view'))
        else:
            sweetness = data.sweetness
            cool = data.cool
            gain = data.gain
            description = data.description
            description = description.replace('<br/>', '\n')
            description = description.replace('&nbsp', ' ')
            def_sweetness = ['', '', '', '', '', '']
            def_cool = ['', '', '', '', '', '']
            def_gain = ['', '', '', '', '', '']
            for i in range(1, 6):
                if i == sweetness:
                    def_sweetness[i] = 'checked'
            for i in range(1, 6):
                if i == cool:
                    def_cool[i] = 'checked'
            for i in range(1, 6):
                if i == gain:
                    def_gain[i] = 'checked'
            return render_template('edit_evaluation.html', def_sweetness=def_sweetness, def_cool=def_cool,
                                   def_gain=def_gain,
                                   description=description)
    else:
        data = request.form
        sweetness = data.get('sweet')
        cool = data.get('cool')
        gain = data.get('gain')
        description = data.get('description')
        error = False
        if not sweetness:
            flash('請選擇甜度', 'error')
            error = True
        if not cool:
            flash('請選擇涼度', 'error')
            error = True
        if not gain:
            flash('請選擇收穫', 'error')
            error = True
        if not description:
            flash('請輸入評價', 'error')
            error = True
        if not error:
            Evaluation.query.filter_by(username='40711014e', course_id='1').update(dict(sweetness=sweetness))
            Evaluation.query.filter_by(username='40711014e', course_id='1').update(dict(cool=cool))
            Evaluation.query.filter_by(username='40711014e', course_id='1').update(dict(gain=gain))
            Evaluation.query.filter_by(username='40711014e', course_id='1').update(dict(description=description))
            db.session.commit()
            flash('評價更新成功', 'success')
            return redirect(url_for('evaluation_bp.view'))
        else:
            return redirect(url_for('evaluation_bp.edit'))

