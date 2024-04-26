import datetime

from src.entity.UserBehavior import UserBehavior


class UserBehaviorDTO(UserBehavior):
    def __init__(self, id: str = None, user_code: str = None, phone_id: int = None,
                 create_time: datetime.datetime = None, like_count: int = None, img_url: str = None,
                 param_url: str = None):
        super().__init__(id, user_code, phone_id, create_time, like_count)
        self.img_url = img_url
        self.param_url = param_url
