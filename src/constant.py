import logging

# 调试单个代码的时候改为  ../../   启动整个APP的时候改为../
PROJECT_DIR = "../"

# 爬虫线程数量，根据电脑cpu性能而定
THREAD_CORE_NUM = 10
# 获取参数的子线程,cpu足够强大的话就往大了配
SECOND_THREAD_CORE_NUM = 20
# 日志打印级别
LOG_LEVEL = logging.INFO
# session 失效时间 60s,配置为-1 则永远不失效
SESSION_TIME_OUT = -1
# 是否开启session校验
SESSION_VALID = False
# 白名单列表
WHITE_URL_LIST = ["/sys_user/login", "/sys_user/add_user"]
# 是否开启爬虫任务
CLIMB_TASK = False
CLIMB_ONCE = False
# 多久执行一次，单位分钟
CLIMB_MIN_SEP = 60

MYSQL = "mysql"
SQLITE = "sqlite"
SESSION_ID = "Session-Id"
IS_TEST = False

LOG_PATH = PROJECT_DIR + "log/log.txt"
CONFIG_PATH = PROJECT_DIR + "conf/conf.json"
mobile_type_data_path = PROJECT_DIR + 'data/mobile/mobile_type.csv'  # 存放各种手机类型的文件，起始文件
mobile_data_path = PROJECT_DIR + 'data/mobile/mobile_data'  # 存放各种手机url以及简单参数的目录
evaluate_data_path = PROJECT_DIR + 'data/mobile/mobile_evaluate'  # 存放评论的目录
param_data_path = PROJECT_DIR + 'data/mobile/mobile_param'  # 存放参数的目录
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
