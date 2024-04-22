from datetime import datetime

from src.entity.Article import Article
from src.entity.Comment import Comment


class ArticleDTO(Article):
    def __init__(self, article_id=None, user=None, article_content=None, article_picture=None,
                 article_time=datetime.now(), comment_list: list[Comment] = None):
        super().__init__(article_id, user, article_content, article_picture, article_time)
        self.comment_list = comment_list
