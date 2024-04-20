from datetime import datetime


class Article:
    def __init__(self, article_id=None, user=None, article_content=None, article_picture=None,
                 article_time=datetime.now()):
        self.article_id = article_id
        self.user = user
        self.article_content = article_content
        self.article_picture = article_picture
        self.article_time = article_time
