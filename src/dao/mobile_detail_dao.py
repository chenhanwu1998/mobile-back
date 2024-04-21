from src.dao.SingleUtils import SingleUtils
from src.entity.MobileDetail import MobileDetail
from src.utils import string_utils, common_utils
from src.utils.loging_utils import logger


def select_mobile_detail_by_condition(mobile: MobileDetail, order_col: str = None,
                                      limit: int = None, not_none_col: list = None) -> list[MobileDetail]:
    sql = "select * from mobile_detail"
    where_sql = common_utils.get_where_sql(mobile, True)
    if not_none_col is not None and len(not_none_col) != 0:
        not_none_condition = []
        for col in not_none_col:
            not_none_condition.append(f"{col} is not null and {col} !='None' and {col} !=''")
        condition = string_utils.join(not_none_condition, sep=" and ")
        if not string_utils.is_empty(where_sql):
            where_sql += f"and ({condition})"
        else:
            where_sql = condition
    if not string_utils.is_empty(where_sql):
        sql += " where " + where_sql
    if order_col is not None:
        sql += f" order by {order_col} desc "
    if limit is not None:
        sql += f" limit {limit}"
    logger.info("sql:" + sql)
    return trans_result(sql)


def select_by_mobile_ids(mobile_ids: list) -> list[int]:
    value_str = string_utils.join(mobile_ids)
    sql = f"select id from mobile_detail where id in ({value_str})"
    result = SingleUtils.mysql_utils.query_sql(sql)
    target_res = [temp[0] for temp in result]
    return target_res


def add_batch(mobile_list: list[MobileDetail]) -> bool:
    temp = mobile_list[0]
    temp_dict = temp.__dict__
    key_str = string_utils.join(list(temp_dict.keys()))
    value_str = string_utils.join_obj_value_list(mobile_list)
    sql = f"insert into mobile_detail ({key_str}) values {value_str}"
    sql = sql.replace("%", "%%")
    logger.debug("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


# 一条一条更新，性能问题的话就换为批量操作
def update_batch(mobile_list: list[MobileDetail]) -> bool:
    for temp in mobile_list:
        temp_dict = temp.__dict__
        value_str = string_utils.join_dict(temp_dict)
        sql = f"update  mobile_detail set {value_str} where id = '{temp.id}'"
        sql = sql.replace("%", "%%")
        logger.debug("sql:" + sql)
        SingleUtils.mysql_utils.update_sql(sql)
    return True


def trans_result(sql: str) -> list[MobileDetail]:
    temp_dict = MobileDetail().__dict__
    conn = SingleUtils.mysql_utils.get_connect()
    temp_result = conn.execute(sql)
    result = temp_result.columns(*temp_dict.keys())
    mobile_list = []
    for temp in result:
        mobile_list.append(MobileDetail(*temp))
    return mobile_list


if __name__ == '__main__':
    res = select_mobile_detail_by_condition(MobileDetail(company_type="vivo"), limit=10)
    common_utils.print_obj_list(res)
