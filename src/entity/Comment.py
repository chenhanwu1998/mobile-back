from datetime import datetime


class Comment:
    def __init__(self, comment_id=None, comment_content=None, user=None, article_id=None, update_time=datetime.now()):
        self.comment_id = comment_id
        self.comment_content = comment_content
        self.user = user
        self.article_id = article_id
        self.update_time = update_time
