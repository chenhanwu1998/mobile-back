from datetime import datetime

from src.entity.SysUser import SysUser


class SysUserDTO(SysUser):
    def __init__(self, user_code: str, pswd: str = None, e_mail: str = None, stu_id: str = None, question: str = None,
                 answer: str = None, dates: datetime = datetime.now(), session_id: str = None, user_photo: str = None):
        super().__init__(user_code, pswd, e_mail, stu_id, question, answer, dates, user_photo)
        self.session_id = session_id
