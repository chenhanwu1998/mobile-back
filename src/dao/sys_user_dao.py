from src.dao.SingleUtils import SingleUtils
from src.entity.SysUser import SysUser
from src.utils import string_utils, common_utils
from src.utils.loging_utils import logger


def select_user_by_condition(user: SysUser) -> list:
    sql = "select * from sys_user"
    where_sql = common_utils.get_where_sql(user)
    if not string_utils.is_empty(where_sql):
        sql += " where " + where_sql
    logger.info("sql:" + sql)
    return trans_result(sql)


def select_user_photo_dict(user_code_list: set) -> dict:
    if user_code_list is None or len(user_code_list) == 0:
        return dict()
    value_str = string_utils.join(user_code_list, trans_str=True)
    sql = f"select * from sys_user where  user_code in ({value_str})"
    logger.info("sql:" + sql)
    user_list = trans_result(sql)
    data_dict = dict()
    for user in user_list:
        data_dict[user.user_code] = user.user_photo
    return data_dict


def add_user(user: SysUser) -> bool:
    entity_dict = user.__dict__
    key_str = string_utils.join(list(entity_dict.keys()), False)
    value_str = string_utils.join(list(entity_dict.values()), True)
    sql = f"insert into sys_user ({key_str}) values ({value_str})"
    logger.info("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def update_by_user_code(user: SysUser) -> bool:
    if string_utils.is_empty(user.user_code):
        return False
    value_str = string_utils.join_dict(user.__dict__)
    sql = f"update sys_user set {value_str} where user_code = '{user.user_code}'"
    logger.info("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def trans_result(sql: str) -> list:
    temp_dict = SysUser().__dict__
    conn = SingleUtils.mysql_utils.get_connect()
    result = conn.execute(sql).columns(*temp_dict.keys())
    user_list = []
    for temp in result:
        user_list.append(SysUser(*temp))
    return user_list


if __name__ == '__main__':
    # update_by_user_code(SysUser('chenhw3', '5555555', 'czcz'))
    res = select_user_by_condition(SysUser('chenhw3'))
    common_utils.print_obj_list(res)
