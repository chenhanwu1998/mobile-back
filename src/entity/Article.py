import datetime


class Article:
    def __init__(self, article_id=None, user=None, article_content=None, article_picture=None,
                 article_time=None, like_num: int = 0):
        self.article_id = article_id
        self.user = user
        self.article_content = article_content
        self.article_picture = article_picture
        if article_time is None:
            self.article_time = datetime.datetime.now()
        else:
            self.article_time = article_time
        self.like_num = like_num
