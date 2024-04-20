from flask import request, jsonify, Blueprint

from src.dto.Result import Result
from src.entity.SysUser import SysUser
from src.service import sys_user_service
from src.utils import common_utils
from src.utils.loging_utils import logger

sys_user_route = Blueprint('sys_user_route', __name__)


# 定义一个接口
@sys_user_route.route('/sys_user/add_user', methods=['POST'])
def add_user():
    json_data = request.json
    logger.info("json_data:" + str(json_data))
    user = SysUser(**json_data)
    result = sys_user_service.add_user(user)
    return jsonify(Result.success(result).__dict__)


@sys_user_route.route('/sys_user/login', methods=['POST'])
def login():
    json_data = request.json
    logger.info("json_data:" + str(json_data))
    user = SysUser(**json_data)
    result = sys_user_service.user_login(user)
    return jsonify(Result.success(result.__dict__).__dict__)


@sys_user_route.route('/sys_user/logout', methods=['POST'])
def logout():
    json_data = request.json
    logger.info("json_data:" + str(json_data))
    user = SysUser(**json_data)
    result = sys_user_service.user_logout(user)
    return jsonify(Result.success(result).__dict__)


# 定义一个接口
@sys_user_route.route('/sys_user/update_user', methods=['POST'])
def update_user():
    json_data = request.json
    logger.info("json_data:" + str(json_data))
    user = SysUser(**json_data)
    result = sys_user_service.update_by_user_code(user)
    return jsonify(Result.success(result).__dict__)


# 定义一个接口
@sys_user_route.route('/sys_user/select_user_by_condition', methods=['GET'])
def select_user_by_condition():
    # 处理请求的逻辑
    data = request.args.to_dict()  # 从查询参数中获取数据
    logger.info("data:" + str(data))
    user = SysUser(**data)
    result_list = sys_user_service.select_user_by_condition(user)
    return jsonify(Result.success(common_utils.trans_obj_list(result_list)).__dict__)
