from src.cache import cache
from src.dao import sys_user_dao
from src.dto.SysUserDTO import SysUserDTO
from src.entity.SysUser import SysUser
from src.utils import list_utils
from src.utils import string_utils, convert_utils
from src.utils.loging_utils import logger


def user_login(user: SysUser) -> SysUserDTO:
    if string_utils.is_empty(user.user_code):
        raise Exception("用户编码为空")
    user_list = sys_user_dao.select_user_by_condition(SysUser(user_code=user.user_code))
    if list_utils.is_empty(user_list):
        raise Exception("找不到对应的用户信息")
    if len(user_list) > 1:
        raise Exception("用户存在多个，请联系管理员清楚")
    db_user = user_list[0]
    if user.pswd == db_user.pswd:
        session_id = cache.save_cache(db_user)
        user_dto = convert_utils.convert_user(db_user)
        user_dto.session_id = session_id
        logger.info("user_dto:" + str(user_dto.__dict__))
        return user_dto
    else:
        raise Exception("密码错误")


# 注销，清楚缓存
def user_logout(user: SysUser):
    cache.clear_cache_by_user_code(user.user_code)
    return True


def select_user_by_condition(user: SysUser) -> list:
    return sys_user_dao.select_user_by_condition(user)


def add_user(user: SysUser) -> bool:
    result_list = sys_user_dao.select_user_by_condition(SysUser(user_code=user.user_code))
    if len(result_list) != 0:
        raise Exception("用户已经存在")
    return sys_user_dao.add_user(user)


def update_by_user_code(user: SysUser) -> bool:
    if string_utils.is_empty(user.user_code):
        raise Exception("用户编码为空")
    return sys_user_dao.update_by_user_code(user)
