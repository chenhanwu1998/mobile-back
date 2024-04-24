from datetime import datetime

from src.entity.Article import Article
from src.entity.Comment import Comment


class ArticleDTO(Article):
    def __init__(self, article_id=None, user=None, article_content=None, article_picture=None,
                 article_time=datetime.now(), like_num: int = 0, comment_list: list[Comment] = None,
                 user_code_photo_dict: dict = dict):
        super().__init__(article_id, user, article_content, article_picture, article_time, like_num)
        self.comment_list = comment_list
        self.user_code_photo_dict = user_code_photo_dict
