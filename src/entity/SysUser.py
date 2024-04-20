from datetime import datetime


class SysUser:
    def __init__(self, user_code: str = None, pswd: str = None, e_mail: str = None, stu_id: str = None,
                 question: str = None,
                 answer: str = None, dates: datetime = datetime.now()):
        self.user_code = user_code
        self.pswd = pswd
        self.e_mail = e_mail
        self.stu_id = stu_id
        self.question = question
        self.answer = answer
        self.dates = dates



