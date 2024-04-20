import uuid
from datetime import datetime
from typing import Dict

from flask import request

from src.constant import SESSION_TIME_OUT, SESSION_ID
from src.entity.SysUser import SysUser
from src.utils import dict_utils
from src.utils.loging_utils import logger

session_user_info: Dict[str, SysUser] = dict()
session_time_info: Dict[str, datetime] = dict()
user_status_info: Dict[str, str] = dict()

'''
处理session缓存用户信息
'''


def save_cache(user: SysUser) -> str:
    if user.user_code in user_status_info:
        session_id = user_status_info[user.user_code]
    else:
        session_id = str(uuid.uuid4())
    user_status_info[user.user_code] = session_id
    session_user_info[session_id] = user
    session_time_info[session_id] = datetime.now()
    return session_id


def clear_cache_by_user_code(user_code: str) -> bool:
    session_id = user_status_info[user_code]
    return clear_cache(session_id)


def clear_cache(session_id: str) -> bool:
    user = dict_utils.remove(session_user_info, session_id)
    dict_utils.remove(session_time_info, session_id)
    if user is not None:
        dict_utils.remove(user_status_info, user.user_code)
    return True


def refresh_cache(session_id: str) -> bool:
    session_time_info[session_id] = datetime.now()
    return True


# 检查session_id是否存在
def check_session_id(session_id: str) -> bool:
    result = session_id in session_user_info.keys()
    result = result and (session_id in session_time_info.keys())
    if result:
        user_code = session_user_info[session_id].user_code
        result = result and (user_code in user_status_info.keys())
    if not result:
        clear_cache(session_id)
    return result


# 检查session是否过期
# 配置超时时间为-1的时候session永不失效
def check_expired(session_id: str) -> bool:
    session_time = dict_utils.get_value(session_time_info, session_id)
    now_time = datetime.now()
    delta = now_time - session_time
    second = delta.seconds
    logger.info("second:" + str(second))
    if SESSION_TIME_OUT == -1:
        return False
    if second > SESSION_TIME_OUT:
        clear_cache(session_id)
        return True
    return False


def get_session_id():
    if SESSION_ID not in list(request.headers.keys()):
        return None
    session_id = request.headers[SESSION_ID]
    return session_id


def get_user_code():
    session_id = get_session_id()
    user = dict_utils.get_value(session_user_info, session_id)
    if user is not None:
        return user.user_code
    return None
