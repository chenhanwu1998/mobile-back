from flask import request, jsonify, Blueprint

from src.dto.Result import Result
from src.entity.Article import Article
from src.service import article_service
from src.utils import common_utils, convert_utils, string_utils
from src.utils.loging_utils import logger

article_route = Blueprint('article_route', __name__)


# 添加文章
@article_route.route('/article/add_article', methods=['POST'])
def add_article():
    data = request.json
    logger.info("data:", data)
    article_data = Article(**data)
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
