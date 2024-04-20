from src.dao.SingleUtils import SingleUtils
from src.entity.MobileCompany import MobileCompany
from src.utils import string_utils, common_utils
from src.utils.loging_utils import logger


def select_mobile_company_by_condition(company: MobileCompany, order_col: str = None, limit: int = None) -> list:
    sql = "select * from mobile_company"
    where_sql = common_utils.get_where_sql(company)
    if not string_utils.is_empty(where_sql):
        sql += " where " + where_sql
    if order_col is not None:
        sql += f" order by {order_col} desc "
    if limit is not None:
        sql += f" limit {limit}"
    logger.info("sql:" + sql)
    return trans_result(sql)


def add_batch(company_list: list[MobileCompany]) -> bool:
    temp = company_list[0]
    temp_dict = temp.__dict__
    key_str = string_utils.join(list(temp_dict.keys()))
    value_str = string_utils.join_obj_value_list(company_list)
    sql = f"insert into mobile_company ({key_str}) values {value_str}"
    logger.info("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


# 一条一条更新，性能问题的话就换为批量操作
def update_batch(company_list: list[MobileCompany]) -> bool:
    for temp in company_list:
        temp_dict = temp.__dict__
        value_str = string_utils.join_dict(temp_dict)
        sql = f"update  mobile_company set {value_str} where brand = '{temp.brand}'"
        SingleUtils.mysql_utils.update_sql(sql)
    return True


def trans_result(sql: str) -> list:
    temp_dict = MobileCompany().__dict__
    conn = SingleUtils.mysql_utils.get_connect()
    result = conn.execute(sql).columns(*temp_dict.keys())
    mobile_list = []
    for temp in result:
        mobile_list.append(MobileCompany(*temp))
    return mobile_list


if __name__ == '__main__':
    res = select_mobile_company_by_condition(MobileCompany('vivo'), 10)
    # update_batch([])
    common_utils.print_obj_list(res)
