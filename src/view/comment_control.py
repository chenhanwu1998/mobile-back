import datetime

from flask import request, jsonify, Blueprint

from src.dto.Result import Result
from src.entity.Comment import Comment
from src.service import comment_service
from src.utils import common_utils, convert_utils
from src.utils.loging_utils import logger

comment_route = Blueprint('comment_route', __name__)


# 定义一个接口
@comment_route.route('/comment/add_comment', methods=['POST'])
def add_comment():
    # 处理请求的逻辑
    data = request.json
    logger.info("data:" + str(data))
    comment = Comment(**data)
    comment.update_time = datetime.datetime.now()
    result = comment_service.add_comment(comment)
    return jsonify(Result.success(result).__dict__)


# 定义一个接口
@comment_route.route('/comment/update_comment', methods=['POST'])
def update_comment():
    # 处理请求的逻辑
    data = request.json
    logger.info("data:" + str(data))
    comment = Comment(**data)
    comment.update_time = datetime.datetime.now()
    result = comment_service.update_comment_by_id(comment)
    return jsonify(Result.success(result).__dict__)


# 定义一个接口
@comment_route.route('/comment/delete_comment', methods=['POST'])
def delete_comment():
    # 处理请求的逻辑
    data = request.json
    logger.info("data:" + str(data))
    comment = Comment(**data)
    result = comment_service.delete_comment_by_id(comment.comment_id)
    return jsonify(Result.success(result).__dict__)


# 定义一个接口
@comment_route.route('/comment/select_comment_by_condition', methods=['GET'])
def select_comment_by_condition():
    # 处理请求的逻辑
    data = request.args.to_dict()
    logger.info("data:" + str(data))
    limit = None
    if "limit" in data.keys():
        limit = data["limit"]

    data_dict = convert_utils.convert_dict(Comment(), data)
    comment = Comment(**data_dict)
    result_list = comment_service.select_comment_by_condition(comment, limit)
    return jsonify(Result.success(common_utils.trans_obj_list(result_list)).__dict__)
