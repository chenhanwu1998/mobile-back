from datetime import datetime


class Comment:
    def __init__(self, comment_id=None, comment_content=None, user=None, article_id=None, update_time: datetime = None,
                 to_user: str = None, comment_status: str = None):
        self.comment_id = comment_id
        self.comment_content = comment_content
        self.user = user
        self.article_id = article_id
        if update_time is None:
            self.update_time = datetime.now()
        else:
            self.update_time = update_time
        self.to_user = to_user
        self.comment_status = comment_status
