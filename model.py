from share.db import db

takes = db.Table(
    'takes',
    db.Column('username', db.String(30), db.ForeignKey('user.username'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.cid'), primary_key=True)
)


class User(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    dept_name = db.Column(db.String(80), default='')
    grade = db.Column(db.Integer, default=0)
    courses = db.relationship('Course', secondary=takes, backref=db.backref('user'))

    def __init__(self, username, email, password, dept_name, grade, is_admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.dept_name = dept_name
        self.grade = grade
        self.is_admin = is_admin

    def __str__(self):
        return f'email: {self.email} username: {self.email} password: {self.password} is_admin: {self.is_admin} dept_name: {self.dept_name} grade: {self.grade}'


class Course(db.Model):
    cid = db.Column(db.Integer, primary_key=True)  # 課程 ID
    course_code = db.Column(db.String(128))  # 科目代碼
    serial_no = db.Column(db.String(128))  # 開課序號
    course_name = db.Column(db.String(128))  # 課程名稱
    department = db.Column(db.String(128))  # 開課單位
    reg_sel = db.Column(db.String(32))  # 必/選修
    credits = db.Column(db.Integer)  # 學分數
    restrict = db.Column(db.String(128))  # 限修條件
    time = db.Column(db.String(128))  # 上課時間
    location = db.Column(db.String(128))  # 上課地點
    instructor = db.Column(db.String(128))  # 授課教師
    year = db.Column(db.Integer)  # 學年
    term = db.Column(db.Integer)  # 學期
    quota = db.Column(db.Integer)  # 限修人數
    authorize_quota = db.Column(db.Integer)  # 授權碼人數
    interschool_quota = db.Column(db.Integer)  # 校際人數
    english = db.Column(db.String(128))  # 英語授課
    dept_code = db.Column(db.String(128))  # 系代碼
    note = db.Column(db.String(128))  # 備註

    def __init__(self, course_code, serial_no, course_name, department, reg_sel, credits, restrict, time, location, instructor,
                 year, term, quota, authorize_quota, interschool_quota, english, dept_code, note):
        self.course_code = course_code
        self.serial_no = serial_no
        self.course_name = course_name
        self.department = department
        self.reg_sel = reg_sel
        self.credits = credits
        self.restrict = restrict
        self.time = time
        self.location = location
        self.instructor = instructor
        self.year = year
        self.term = term
        self.quota = quota
        self.authorize_quota = authorize_quota
        self.interschool_quota = interschool_quota
        self.english = english
        self.dept_code = dept_code
        self.note = note


class Evaluation(db.Model):
    eid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.ForeignKey('user.username'), nullable=False)
    course_id = db.Column(db.ForeignKey('course.cid'), nullable=False)
    description = db.Column(db.String(512))
    sweetness = db.Column(db.Integer, nullable=False)
    cool = db.Column(db.Integer, nullable=False)
    gain = db.Column(db.Integer, nullable=False)
    course = db.relationship('Course', backref=db.backref('evaluation'))
    user = db.relationship('User', backref=db.backref('evaluation'))

    def __init__(self, username, course_id, description, sweetness, cool, gain):
        self.username = username
        self.course_id = course_id
        self.description = description
        self.sweetness = sweetness
        self.cool = cool
        self.gain = gain
