from flask import request, jsonify, Blueprint

from src.dto.Result import Result
from src.entity.MobileDetail import MobileDetail
from src.service import mobile_detail_service
from src.utils import common_utils, convert_utils
from src.utils.loging_utils import logger

mobile_detail_route = Blueprint('mobile_detail_route', __name__)


@mobile_detail_route.route('/mobile_detail/select_mobile_detail_by_condition', methods=['GET'])
def select_mobile_detail_by_condition():
    data = request.args.to_dict()
    logger.info("data:" + str(data))
    limit = None
    if "limit" in data.keys() and data["limit"] is not None:
        limit = int(data["limit"])
    data_dict = convert_utils.convert_dict(MobileDetail(), data)
    mobile_detail = MobileDetail(**data_dict)

    order_col = None
    if "order_col" in data.keys():
        order_col = data["order_col"]

    result = mobile_detail_service.select_mobile_detail_by_condition(mobile_detail, order_col, limit)
    return jsonify(Result.success(common_utils.trans_obj_list(result)).__dict__)
