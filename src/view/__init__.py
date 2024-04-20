from src.view.article_control import article_route
from src.view.comment_control import comment_route
from src.view.mobile_company_control import mobile_company_route
from src.view.mobile_detail_control import mobile_detail_route
from src.view.sys_user_control import sys_user_route

blueprints = [sys_user_route, mobile_detail_route, article_route, comment_route, mobile_company_route]


def register_blueprints(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix='/')
