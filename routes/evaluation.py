from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.sql import func
from model import Evaluation, Course
from share.login import login_required, admin_required
from share.db import db


evaluation_bp = Blueprint('evaluation_bp', __name__)


@evaluation_bp.route('/view/<cid>', methods=['GET'])
def view(cid):
    if request.method == 'GET':
        # 課程資訊
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
        avg_sweetness = Evaluation.query.with_entities(func.avg(Evaluation.sweetness)).filter(
            Evaluation.course_id == cid).first()
        avg_cool = Evaluation.query.with_entities(func.avg(Evaluation.cool)).filter(Evaluation.course_id == cid).first()
        avg_gain = Evaluation.query.with_entities(func.avg(Evaluation.gain)).filter(Evaluation.course_id == cid).first()
        # 課程評價
        evaluation_data = course_data.evaluation
        for eva_data in evaluation_data:
            eva_data.description = eva_data.description.split('\n')
        return render_template('view_evaluation.html', cid=cid, evaluation_data=evaluation_data,
                               avg_sweetness=avg_sweetness[0], avg_cool=avg_cool[0], avg_gain=avg_gain[0],
                               serial_no=serial_no, term=term,
                               year=year, department=department, course_name=course_name, course_code=course_code,
                               restrict=restrict, quota=quota, authorize_quota=authorize_quota,
                               interschool_quota=interschool_quota, instructor=instructor, reg_sel=reg_sel,
                               credits=credits, english=english, time=time, location=location, note=note)


@evaluation_bp.route('/add/<cid>', methods=['GET', 'POST'])
@login_required
def add(user, cid):
    if request.method == 'GET':
        checkdata = Evaluation.query.filter_by(username=user.username, course_id=cid).first()
        error = False
        if checkdata:
            flash('已有評價紀錄，如欲編輯評價請點選 "編輯評價"', 'error')
            error = True
            return redirect(url_for('evaluation_bp.view', cid=cid))
        else:
            return render_template('add_evaluation.html', cid=cid)
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
        if len(description) > 512:
            flash('評價勿輸入超過512個字元', 'error')
            error = True
        if not error:
            evaluation = Evaluation(username=user.username, course_id=cid, sweetness=sweetness, cool=cool, gain=gain,
                                    description=description)
            db.session.add(evaluation)
            db.session.commit()
            flash('評價儲存成功', 'success')
            return redirect(url_for('evaluation_bp.view', cid=cid))
        else:
            return redirect(url_for('evaluation_bp.add', cid=cid))


@evaluation_bp.route('/edit/<cid>', methods=['GET', 'POST'])
@login_required
def edit(user, cid):
    if request.method == 'GET':
        data = Evaluation.query.filter_by(username=user.username, course_id=cid).first()
        error = False
        if not data:
            flash('查無評價紀錄，如欲新增評價請點選 "新增評價"', 'error')
            error = True
            return redirect(url_for('evaluation_bp.view', cid=cid))
        else:
            sweetness = data.sweetness
            cool = data.cool
            gain = data.gain
            description = data.description
            def_sweetness = ['']*6
            def_cool = ['']*6
            def_gain = ['']*6
            def_sweetness[sweetness] = 'checked'
            def_cool[cool] = 'checked'
            def_gain[gain] = 'checked'
            return render_template('edit_evaluation.html', cid=cid, def_sweetness=def_sweetness, def_cool=def_cool,
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
        if len(description) > 512:
            flash('評價勿輸入超過512個字元', 'error')
            error = True
        if not error:
            Evaluation.query.filter_by(username=user.username, course_id=cid).update(dict(sweetness=sweetness))
            Evaluation.query.filter_by(username=user.username, course_id=cid).update(dict(cool=cool))
            Evaluation.query.filter_by(username=user.username, course_id=cid).update(dict(gain=gain))
            Evaluation.query.filter_by(username=user.username, course_id=cid).update(dict(description=description))
            db.session.commit()
            flash('評價更新成功', 'success')
            return redirect(url_for('evaluation_bp.view', cid=cid))
        else:
            return redirect(url_for('evaluation_bp.edit', cid=cid))


@evaluation_bp.route('/delete/<cid>', methods=['GET', 'POST'])
@login_required
def delete_evaluation(user, cid):
    data = Evaluation.query.filter_by(username=user.username, course_id=cid).first()
    db.session.delete(data)
    db.session.commit()
    flash('評價刪除成功', 'success')
    return redirect(url_for('evaluation_bp.view', cid=cid))
