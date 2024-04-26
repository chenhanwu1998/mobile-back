import datetime


class UserBehavior:
    def __init__(self, id: str = None, user_code: str = None, phone_id: int = None,
                 create_time: datetime.datetime = None, like_count: int = None):
        self.id = id
        self.user_code = user_code
        self.phone_id = phone_id
        self.create_time = create_time
        self.like_count = like_count
