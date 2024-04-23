import base64
import datetime
import traceback

from src.dto.ArticleDTO import ArticleDTO
from src.utils import string_utils
from src.utils.loging_utils import logger


def get_where_sql(entity, is_like: bool = False, like_list=None) -> str:
    if like_list is None:
        like_list = []
    data_dict = entity.__dict__
    condition_list = []
    for k, v in data_dict.items():
        if not isinstance(v, str) or v is None or string_utils.is_empty(v):
            continue
        if is_like or (like_list is not None and k in like_list):
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


def trans_photo(img_path: str) -> str:
    try:
        with open(img_path, 'rb') as file:
            encode_str = base64.b64encode(file.read()).decode("utf-8")
    except Exception as exc:
        traceback.print_exc()
        logger.error("[文件获取异常]:" + str(exc))
        encode_str = ""
    suffix = img_path.split(".")[-1]
    if string_utils.is_empty(suffix):
        suffix = "jog"
    prefix = f"data:image/{suffix};base64,"
    return prefix + encode_str


base_type = [str, list, dict, int, float, datetime.datetime]


def check_type(obj) -> bool:
    for b_type in base_type:
        if isinstance(obj, b_type):
            return True
    return False


def trans_obj_to_dict(obj: object) -> dict():
    if isinstance(obj, list):
        for list_cell in obj:
            if check_type(list_cell):
                continue
