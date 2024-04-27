import datetime
import os
import random
import uuid

from flask import request, jsonify, Blueprint

from src.constant import uer_photo_dir_path
from src.dto.Result import Result
from src.entity.SysUser import SysUser
from src.entity.UserBehavior import UserBehavior
from src.service import sys_user_service
from src.service import user_behavior_service
from src.utils import common_utils, convert_utils, string_utils
from src.utils.loging_utils import logger

sys_user_route = Blueprint('sys_user_route', __name__)

default_user_path = "default-user-img"
default_user_photo_list = ['default-user-img1.jpg',
                           'default-user-img2.jpg',
                           'default-user-img3.jpg',
                           'default-user-img5.jpg',
                           'default-user-img4.jpg']


# 定义一个接口
@sys_user_route.route('/sys_user/add_user', methods=['POST'])
def add_user():
    json_data = request.json
    logger.info("json_data:" + str(json_data))
    user = SysUser(**json_data)
    # 随机设置默认用户头像
    rand = random.Random().randint(1, 5)
    default_user_img = uer_photo_dir_path + f"/{default_user_path}{rand}.jpg"
    user.user_photo = default_user_img
    user.dates = datetime.datetime.now()

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
    json_data = dict(request.json)
    logger.info("json_data:" + str(json_data))
    if "new_password" not in json_data.keys():
        raise Exception("缺失新密码")
    user_dict = convert_utils.convert_dict(SysUser(), json_data)
    user = SysUser(**user_dict)
    result = sys_user_service.update_by_user_code(user, json_data["new_password"])
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


@sys_user_route.route('/sys_user/update_user_photo', methods=['POST'])
def update_user_photo():
    data = request.form.to_dict()
    logger.info("data:" + str(data))
    if "file" not in request.files.keys():
        raise Exception("缺乏用户头像")
    file = request.files['file']
    file_path = uer_photo_dir_path + "/" + str(uuid.uuid4()) + "_" + file.filename
    file.save(file_path)
    request.from_values()
    sys_user = SysUser(**data)
    old_user_photo_path = sys_user.user_photo
    sys_user.user_photo = file_path
    sys_user_service.update_user_photo(sys_user)
    old_photo_name = old_user_photo_path.split("/")[-1]
    if not string_utils.is_empty(old_user_photo_path) and old_photo_name not in default_user_photo_list:
        os.remove(old_user_photo_path)
    return jsonify(Result.success(file_path).__dict__)


@sys_user_route.route("/sys_user/select_user_behavior", methods=["POST"])
def select_user_behavior():
    data = dict(request.json)
    logger.info("data:" + str(data))
    limit = None
    if "limit" in data.keys():
        limit = data["limit"]
    data_dict = convert_utils.convert_dict(UserBehavior(), data)
    condition = UserBehavior(**data_dict)
    result = user_behavior_service.select_user_by_condition(condition, limit)
    return jsonify(Result.success(common_utils.trans_obj_list(result)).__dict__)


# 新增或者更新用户行为
@sys_user_route.route("/sys_user/add_or_update_user_behavior", methods=["POST"])
def add_or_update_user_behavior():
    data = dict(request.json)
    logger.info("data:" + str(data))
    data_dict = convert_utils.convert_dict(UserBehavior(), data)
    user_behavior = UserBehavior(**data_dict)
    result = user_behavior_service.add_or_update_user_behavior(user_behavior)
    return jsonify(Result.success(result).__dict__)
