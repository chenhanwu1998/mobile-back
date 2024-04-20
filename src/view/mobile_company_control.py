from flask import request, jsonify, Blueprint

from src.dto.Result import Result
from src.entity.MobileCompany import MobileCompany
from src.service import mobile_company_service
from src.utils import common_utils, convert_utils
from src.utils.loging_utils import logger

mobile_company_route = Blueprint('mobile_company_route', __name__)


# 定义一个接口
@mobile_company_route.route('/mobile_company/select_mobile_company_by_condition', methods=['GET'])
def select_mobile_company_by_condition():
    # 处理请求的逻辑
    data = request.args.to_dict()
    logger.info("data:" + str(data))
    limit = None
    if "limit" in data.keys() and data["limit"] is not None:
        limit = int(data["limit"])
    order_col = None
    if "order_col" in data.keys():
        order_col = data["order_col"]

    data_dict = convert_utils.convert_dict(MobileCompany(), data)
    mobile_company = MobileCompany(**data_dict)

    result = mobile_company_service.select_mobile_company_by_condition(mobile_company, order_col, limit)
    return jsonify(Result.success(common_utils.trans_obj_list(result)).__dict__)
