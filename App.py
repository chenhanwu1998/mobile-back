import threading
import traceback

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from src.cache import cache
from src.climb.climb_task import climb
from src.constant import WHITE_URL_LIST, SESSION_ID, SESSION_VALID, CLIMB_TASK, CLIMB_MIN_SEP, CLIMB_ONCE
from src.dto.Result import Result
from src.exception.AuthException import AuthException
from src.utils.loging_utils import logger
from src.view import register_blueprints

app = Flask(__name__)
# 设置跨域
CORS(app, resources="/*")
# 注册所有蓝图（即接口）
register_blueprints(app)

# 异步执行
if CLIMB_ONCE:
    logger.info("开启一次爬虫")
    task = threading.Thread(target=climb)
    task.start()
    # 等待爬虫完毕才启动app
    # task.join()

# 添加定时任务,开启了一次爬虫就默认不进行定时任务爬取
if not CLIMB_ONCE and CLIMB_TASK:
    scheduler = BackgroundScheduler()
    scheduler.add_job(climb, 'interval', minutes=CLIMB_MIN_SEP)
    scheduler.start()


@app.route('/')
def index():
    return render_template('index.html')


# 这里的Exception可以替换为特定的异常类型来处理不同类型的错误
@app.errorhandler(Exception)
def handle_exception(error):
    trace = traceback.format_exc()
    logger.info("request.url:" + request.url)
    logger.error("[全局异常]:" + str(error))
    logger.error("[trace]:" + trace)
    if isinstance(error, AuthException):
        return jsonify(Result.fail_401(str(error)).__dict__), 200
    return jsonify(Result.fail(str(error)).__dict__), 200


# session拦截器,目前暂时使用内存来session存放，可考虑换为redis缓存
@app.before_request
def interceptor():
    if not SESSION_VALID:
        return
    # 跨域校验请求的OPTIONS 不需要校验session
    if "OPTIONS" == request.method:
        return
    logger.debug("header:" + str(request.headers))
    logger.debug("method:" + request.method)
    req_url = request.url
    for url in WHITE_URL_LIST:
        if url in req_url:
            logger.debug("白名单url，不用校验session信息")
            return
    logger.info("req_url:" + req_url)
    if SESSION_ID not in list(request.headers.keys()):
        raise AuthException("缺乏session登录信息")
    session_id = request.headers[SESSION_ID]
    logger.debug(SESSION_ID + ":" + str(session_id))
    if not cache.check_session_id(session_id):
        raise AuthException("未登录")
    if cache.check_expired(session_id):
        raise AuthException("登录过期了")
    # 刷新session时间
    cache.refresh_cache(session_id)


# @app.after_request
# def func_res(resp):
#     res = make_response(resp)
#     res.headers['Access-Control-Allow-Origin'] = '*'
#     res.headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET, POST, PUT, DELETE'
#     res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
#     return res


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
    app.run(host="127.0.0.1", port=5000, debug=False)
