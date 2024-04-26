from src.dao import mobile_detail_dao
from src.dao import user_behavior_dao
from src.dto.UserBehaviorDTO import UserBehaviorDTO
from src.entity.MobileDetail import MobileDetail
from src.entity.UserBehavior import UserBehavior
from src.utils import common_utils


def select_user_by_condition(user: UserBehavior, limit: int = None) -> list[UserBehaviorDTO]:
    res_list = user_behavior_dao.select_user_by_condition(user, limit)
    if res_list is None or len(res_list) == 0:
        model_detail_list = mobile_detail_dao.select_mobile_detail_by_condition(MobileDetail(), order_col="id", limit=5,
                                                                                not_none_col=["cpu", "img_url",
                                                                                              "param_url"])
        res_list = []
        for model_detail in model_detail_list:
            res_list.append(UserBehaviorDTO(phone_id=model_detail.id, param_url=model_detail.param_url,
                                            img_url=model_detail.img_url))
    return res_list


def add_or_update_user_behavior(user_behavior: UserBehavior) -> bool:
    res_list = user_behavior_dao.select_by_user_code_and_mobile_id(user_behavior.user_code, user_behavior.phone_id)
    if res_list is None or len(res_list) == 0:
        user_behavior_dao.add_user_behavior(user_behavior)
    else:
        old_user_behavior = res_list[0]
        user_behavior.like_count = old_user_behavior.like_count + 1
        user_behavior_dao.update_by_user_code_phone(user_behavior)
    return True


if __name__ == '__main__':
    add_or_update_user_behavior(UserBehavior(user_code="chenhanwu", phone_id=31314))
    add_or_update_user_behavior(UserBehavior(user_code="chenhanwu", phone_id=32746))
    res = select_user_by_condition(UserBehavior(user_code="chenhanwu"))
    common_utils.print_obj_list(res)
