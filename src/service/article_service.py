from src.dao import article_dao, comment_dao
from src.entity.Article import Article


def select_article_by_condition(article: Article) -> list:
    return article_dao.select_article_by_condition(article)


def add_article(article: Article) -> bool:
    return article_dao.add_article(article)


def update_article_by_id(article: Article) -> bool:
    return article_dao.update_article_by_id(article)


def delete_article_by_id(article_id: int) -> bool:
    result = article_dao.delete_article_by_id(article_id)
    comment_dao.delete_comment_by_article_id(article_id)
    return result
