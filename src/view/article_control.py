import uuid
from datetime import datetime

from flask import request, jsonify, Blueprint, send_file

from src.constant import forum_photo_dir_path
from src.dto.Result import Result
from src.entity.Article import Article
from src.service import article_service
from src.utils import common_utils, convert_utils, string_utils
from src.utils.loging_utils import logger

article_route = Blueprint('article_route', __name__)


# 添加文章
@article_route.route('/article/add_article', methods=['POST'])
def add_article():
    data = request.form.to_dict()
    logger.info("data:" + str(data))
    if "file" not in request.files.keys():
        raise Exception("缺乏论坛图片")
    file = request.files['file']
    file_path = forum_photo_dir_path + "/" + str(uuid.uuid4()) + "_" + file.filename
    file.save(file_path)
    request.from_values()
    article_data = Article(**data)
    article_data.article_time = datetime.now()
    article_data.article_picture = file_path
    result = article_service.add_article(article_data)
    return jsonify(Result.success(result).__dict__)


# 更新文章
@article_route.route('/article/update_article', methods=['POST'])
def update_article():
    data = request.json
    logger.info("data:" + str(data))
    article_data = Article(**data)
    result = article_service.update_article_by_id(article_data)
    return jsonify(Result.success(result).__dict__)


# 更新文章
@article_route.route('/article/delete_article', methods=['POST'])
def delete_article():
    data = request.json
    logger.info("data:" + str(data))
    article_data = Article(**data)
    result = article_service.delete_article_by_id(article_data.article_id)
    return jsonify(Result.success(result).__dict__)


# 更新文章
@article_route.route('/article/select_article_by_condition', methods=['GET'])
def select_article_by_condition():
    data = request.args.to_dict()
    logger.info("data:" + str(data))
    limit = None
    if "limit" in data.keys() and not string_utils.is_empty(data["limit"]):
        limit = data["limit"]
    data_dict = convert_utils.convert_dict(Article(), data)
    article_data = Article(**data_dict)
    result_list = article_service.select_article_by_condition(article_data, limit)
    return jsonify(Result.success(common_utils.trans_article_list(result_list)).__dict__)


@article_route.route('/article/upload_article_photo', methods=['POST'])
def upload_article_photo():
    if "file" not in request.files:
        raise Exception("缺乏论坛图片")
    file = request.files['file']
    logger.info("file_name:" + file.filename)
    file_path = forum_photo_dir_path + "/" + file.filename
    file.save(file_path)
    return jsonify(Result.success(file_path).__dict__)


# 获取base64图片
@article_route.route('/article/get_base64_image', methods=['GET'])
def get_base64_img():
    params = request.args.to_dict()
    if "img_path" not in params.keys():
        raise Exception("缺乏图片路径")
    base64_image = common_utils.trans_photo(params["img_path"])
    return base64_image


# 直接获取二进制图片
@article_route.route('/article/get_img', methods=['GET'])
def get_img():
    params = request.args.to_dict()
    if "img_path" not in params.keys():
        raise Exception("缺乏图片路径")
    return send_file(params["img_path"], mimetype='image/jpeg')
