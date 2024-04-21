from src.dao import mobile_detail_dao
from src.entity.MobileDetail import MobileDetail


def select_mobile_detail_by_condition(mobile: MobileDetail, order_col: str = None, limit: int = None,
                                      not_none_col: list = None, low_price: float = None,
                                      high_price: float = None) -> list:
    return mobile_detail_dao.select_mobile_detail_by_condition(mobile, order_col, limit, not_none_col, low_price,
                                                               high_price)


def save_or_update(mobile_detail_list: list[MobileDetail]) -> bool:
    if mobile_detail_list is None or len(mobile_detail_list) == 0:
        return False
    mobile_id_list = [temp.id for temp in mobile_detail_list]
    db_mobile_id = mobile_detail_dao.select_by_mobile_ids(mobile_id_list)
    # logger.info("db_mobile_id:" + str(db_mobile_id))

    add_mobile_list = []
    update_mobile_list = []
    exist_id = set()
    for temp in mobile_detail_list:
        if int(temp.id) in db_mobile_id:
            update_mobile_list.append(temp)
        else:
            if int(temp.id) in exist_id:
                update_mobile_list.append(temp)
            else:
                add_mobile_list.append(temp)
                exist_id.add(int(temp.id))
    if len(add_mobile_list) != 0:
        mobile_detail_dao.add_batch(add_mobile_list)
    if len(update_mobile_list) != 0:
        mobile_detail_dao.update_batch(update_mobile_list)
    return True
