from flask import Blueprint, render_template, request, redirect, url_for
from model import Evaluation
from share.db import db
evaluation_bp = Blueprint('evaluation_bp', __name__)


@evaluation_bp.route('/view')
def view():
    return render_template('view_evaluation.html')


@evaluation_bp.route('/add')
def add():
    return render_template('add_evaluation.html')


@evaluation_bp.route('/edit')
def edit():
    return render_template('edit_evaluation.html')
