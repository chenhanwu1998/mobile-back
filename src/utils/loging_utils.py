import logging

from src.constant import LOG_PATH, LOG_LEVEL

# 创建一个 logger
logger = logging.getLogger('logger')
logger.setLevel(LOG_LEVEL)

# 创建一个 handler，用于写入日志文件
fh = logging.FileHandler(LOG_PATH, mode="w", encoding='utf-8')
fh.setLevel(LOG_LEVEL)

# 创建一个 handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义 handler 的输出格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(pathname)s - %(lineno)d - [%(thread)d] - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给 logger 添加 handler
logger.addHandler(fh)
logger.addHandler(ch)
