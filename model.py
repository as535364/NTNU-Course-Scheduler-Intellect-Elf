from share.db import db

takes = db.Table(
    'takes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.uid'), primary_key=True),
    db.Column('course_id', db.String(128), db.ForeignKey('course.cid'), primary_key=True)
)


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    dept_name = db.Column(db.String(80), default='')
    grade = db.Column(db.Integer, default=0)
    courses = db.relationship('Course', secondary=takes, backref=db.backref('users'))

    def __init__(self, email, username, password, dept_name, grade, is_admin=False):
        self.email = email
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.dept_name = dept_name
        self.grade = grade

    def __str__(self):
        return f'uid: {self.uid} email: {self.email} username: {self.email} password: {self.password} is_admin: {self.is_admin} dept_name: {self.dept_name} grade: {self.grade}'


class Course(db.Model):
    cid = db.Column(db.String(128), primary_key=True)  # 課程ID
    serial_no = db.Column(db.String(128))  # 科目代碼
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

    def __init__(self, cid, serial_no, course_name, department, reg_sel, credits, restrict, time, location, instructor,
                 year, term, quota, authorize_quota, interschool_quota, english, dept_code, note):
        self.CID = cid
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
    user_id = db.Column(db.ForeignKey('user.uid'), nullable=False)
    course = db.Column(db.ForeignKey('course.cid'), nullable=False)
    description = db.Column(db.String(512))
    sweetness = db.Column(db.Integer, nullable=False)
    cool = db.Column(db.Integer, nullable=False)
    gain = db.Column(db.Integer, nullable=False)

    def __init__(self, eid, description, sweetness, cool, gain):
        self.eid = eid
        self.description = description
        self.sweetness = sweetness
        self.cool = cool
        self.gain = gain
