from src.dto.ArticleDTO import ArticleDTO
from src.utils import string_utils


def get_where_sql(entity, is_like: bool = False) -> str:
    data_dict = entity.__dict__
    condition_list = []
    for k, v in data_dict.items():
        if not isinstance(v, str) or v is None or string_utils.is_empty(v):
            continue
        if is_like:
            condition_list.append(f"{k} like '%%{v}%%'")
        else:
            condition_list.append(f"{k}='{v}'")
    return string_utils.join(condition_list, sep="and")


def print_obj_list(entity_list: list):
    for temp in entity_list:
        print(temp.__dict__)


def trans_obj_list(obj_list) -> list:
    target_list = []
    for temp in obj_list:
        target_list.append(temp.__dict__)
    return target_list


def trans_article_list(article_list: list[ArticleDTO]) -> list:
    target_list = []
    for temp in article_list:
        temp_comment_list = temp.comment_list
        target_comment_list = []
        if temp_comment_list is not None:
            for temp_comment in temp_comment_list:
                target_comment_list.append(temp_comment.__dict__)
        temp.comment_list = target_comment_list
        target_list.append(temp.__dict__)
    return target_list
