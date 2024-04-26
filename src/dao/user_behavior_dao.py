import datetime

from src.dao.SingleUtils import SingleUtils
from src.dto.UserBehaviorDTO import UserBehaviorDTO
from src.entity.UserBehavior import UserBehavior
from src.utils import string_utils, common_utils
from src.utils.loging_utils import logger


def select_user_by_condition(user: UserBehavior, limit: int = None) -> list[UserBehaviorDTO]:
    sql = '''select ub.phone_id, ub.id, ub.user_code, ub.create_time, ub.like_count, md.img_url,md.param_url
            from user_behavior ub
            join mobile_detail md on ub.phone_id = md.id '''
    where_sql = common_utils.get_where_sql(user)
    if not string_utils.is_empty(where_sql):
        sql += " where " + where_sql
    sql += " order by like_count desc, create_time desc"
    if limit is not None:
        sql += f" limit {limit}"
    logger.info("sql:" + sql)
    return trans_result_dto(sql)


def select_by_user_code_and_mobile_id(user_code, phone_id) -> list[UserBehavior]:
    sql = f"select * from user_behavior where user_code='{user_code}' and phone_id = {phone_id}"
    logger.info("sql:" + sql)
    return trans_result(sql)


def add_user_behavior(user_behavior: UserBehavior) -> bool:
    user_behavior.like_count = 1
    user_behavior.create_time = datetime.datetime.now()
    user_behavior.id = SingleUtils.mysql_utils.get_next_id("id", "user_behavior")
    temp_dict = user_behavior.__dict__
    key_list = list(temp_dict.keys())
    value_list = list(temp_dict.values())
    key_str = string_utils.join(key_list)
    value_str = string_utils.join(value_list, trans_str=True)
    sql = f"insert into user_behavior ({key_str}) values ({value_str})"
    logger.info("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def update_by_user_code_phone(user_behavior: UserBehavior) -> bool:
    if string_utils.is_empty(user_behavior.user_code) or user_behavior.phone_id is None:
        return False
    user_behavior.create_time = datetime.datetime.now()
    value_str = string_utils.join_dict(user_behavior.__dict__)
    sql = f"update user_behavior set {value_str} where user_code = '{user_behavior.user_code}' and  phone_id = '{user_behavior.phone_id}'"
    logger.info("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def trans_result(sql: str) -> list:
    temp_dict = UserBehavior().__dict__
    conn = SingleUtils.mysql_utils.get_connect()
    result = conn.execute(sql).columns(*temp_dict.keys())
    user_list = []
    for temp in result:
        user_list.append(UserBehavior(*temp))
    return user_list


def trans_result_dto(sql: str) -> list:
    temp_dict = UserBehaviorDTO().__dict__
    conn = SingleUtils.mysql_utils.get_connect()
    result = conn.execute(sql).columns(*temp_dict.keys())
    user_list = []
    for temp in result:
        user_list.append(UserBehaviorDTO(*temp))
    return user_list


if __name__ == '__main__':
    # add_user_behavior(UserBehavior(user_code="chenhanwu", phone_id=31314))
    # add_user_behavior(UserBehavior(user_code="chenhanwu", phone_id=32746))
    res = select_user_by_condition(UserBehavior(user_code="chenhanwu"))
    common_utils.print_obj_list(res)
