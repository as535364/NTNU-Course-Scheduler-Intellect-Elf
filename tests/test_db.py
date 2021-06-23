from model import User, Course
from share.db import db

u1 = User(email='aa@aa.com', username='user1', password='user1', dept_name='dept1', grade=1)
u2 = User(email='aa@aa.com', username='user2', password='user2', dept_name='dept2', grade=2)

c1 = Course('02UG015', '0944', '生物哲學導論', '通識', '通', 2.0, '',
            '四 3-4', '公館 理圖002','林陳涌', 110, 1, 50, 10, 0, '', 'GU', '')
c2 = Course('03UG012', '0948', '臺灣流行文化', '通識', '通', 2.0, '',
            '三 6-7', '本部 誠101', '莊佳穎', 110, 1, 120, 13, 3, '', 'GU', '')

u1.courses.append(c1)
u1.courses.append(c2)

u2.courses.append(c2)
