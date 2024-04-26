from flask import request, jsonify, Blueprint

from src.dto.Result import Result
from src.entity.MobileDetail import MobileDetail
from src.service import mobile_detail_service
from src.utils import common_utils, convert_utils, string_utils
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
    not_none_col = None
    if "not_none_col" in data.keys():
        not_none_col = data["not_none_col"].split(",")
    low_price = None
    high_price = None
    if "low_price" in data.keys() and not string_utils.is_empty(data["low_price"]):
        low_price = data["low_price"]
    if "high_price" in data.keys() and not string_utils.is_empty(data["high_price"]):
        high_price = data["high_price"]

    result = mobile_detail_service.select_mobile_detail_by_condition(mobile_detail, order_col, limit, not_none_col,
                                                                     low_price, high_price)
    return jsonify(Result.success(common_utils.trans_obj_list(result)).__dict__)


@mobile_detail_route.route('/mobile_detail/select_mobile_num_every_company', methods=['GET'])
def select_mobile_num_every_company():
    result = mobile_detail_service.select_mobile_num_every_company()
    return jsonify(Result.success(common_utils.trans_obj_list(result)).__dict__)


@mobile_detail_route.route('/mobile_detail/select_cpu_num_all', methods=['GET'])
def select_cpu_num_all():
    data = request.args.to_dict()
    logger.info("data:" + str(data))
    limit = None
    if "limit" in data.keys() and data["limit"] is not None:
        limit = int(data["limit"])
    result = mobile_detail_service.select_cpu_num_all(limit)
    return jsonify(Result.success(common_utils.trans_obj_list(result)).__dict__)


@mobile_detail_route.route('/mobile_detail/select_score_by_limit', methods=['GET'])
def select_score_by_limit():
    data = request.args.to_dict()
    logger.info("data:" + str(data))
    limit = None
    if "limit" in data.keys() and data["limit"] is not None:
        limit = int(data["limit"])
    result = mobile_detail_service.select_score_by_limit(limit)
    return jsonify(Result.success(common_utils.trans_obj_list(result)).__dict__)


@mobile_detail_route.route('/mobile_detail/select_by_id', methods=['GET'])
def select_by_id():
    data = request.args.to_dict()
    logger.info("data:" + str(data))
    if "mobile_id" not in data:
        raise Exception("缺乏手机id参数")
    result = mobile_detail_service.select_score_by_limit(int(data["mobile_id"]))
    return jsonify(Result.success(result.__dict__).__dict__)
