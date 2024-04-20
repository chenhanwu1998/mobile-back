from src.dao import comment_dao
from src.entity.Comment import Comment


def select_comment_by_condition(comment: Comment) -> list:
    return comment_dao.select_comment_by_condition(comment)


def add_comment(comment: Comment) -> bool:
    return comment_dao.add_comment(comment)


def update_article_by_id(comment: Comment) -> bool:
    return comment_dao.update_article_by_id(comment)


def delete_comment_by_id(comment_id: int) -> bool:
    return comment_dao.delete_comment_by_id(comment_id)


def delete_comment_by_article_id(article_id: int) -> bool:
    return delete_comment_by_article_id(article_id)
