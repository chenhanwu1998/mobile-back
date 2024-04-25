from src.dao import comment_dao
from src.dao import sys_user_dao
from src.entity.Comment import Comment
from src.utils import convert_utils


def select_comment_by_condition(comment: Comment, limit: int = None) -> list:
    comment_list = comment_dao.select_comment_by_condition(comment, limit)
    user_code_set = set()
    for comment in comment_list:
        user_code_set.add(comment.user)
    user_photo_dict = sys_user_dao.select_user_photo_dict(user_code_set)
    comment_dto_list = []
    for comment in comment_list:
        comment_dto = convert_utils.convert_comment_to_dto(comment)
        if comment.user in user_photo_dict.keys():
            comment_dto.user_photo = user_photo_dict[comment.user]
        comment_dto_list.append(comment_dto)
    return comment_dto_list


def add_comment(comment: Comment) -> bool:
    return comment_dao.add_comment(comment)


def update_comment_by_id(comment: Comment) -> bool:
    return comment_dao.update_comment_by_id(comment)


def delete_comment_by_id(comment_id: int) -> bool:
    return comment_dao.delete_comment_by_id(comment_id)


def delete_comment_by_article_id(article_id: int) -> bool:
    return delete_comment_by_article_id(article_id)
