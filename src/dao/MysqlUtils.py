import json
import traceback

from sqlalchemy import create_engine

from src.constant import CONFIG_PATH, MYSQL, SQLITE
from src.utils.loging_utils import logger


def get_config():
    file = open(CONFIG_PATH, 'r', encoding='utf-8')
    config = json.load(file)
    print("config:", config)
    return config


class MysqlUtils:

    def __init__(self):
        self.connect = None
        self.config = get_config()
        self.engine = None
        self.set_engine()

    def set_engine(self):
        if self.config["DB_TYPE"] == MYSQL:
            self.engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4'
                                        % (self.config['MYSQL_USER'], self.config['MYSQL_PASSWORD'],
                                           self.config['MYSQL_HOST'],
                                           self.config['MYSQL_PORT'], self.config['MYSQL_DB']), )
        elif self.config["DB_TYPE"] == SQLITE:
            self.engine = create_engine('sqlite:///' + self.config["SQLITE_PATH"])
        else:
            raise Exception("数据库配置错误")

    def get_connect(self):
        if self.connect is None:
            self.connect = self.engine
        try:
            self.connect.execute("select 1")
        except Exception as e:
            trace = traceback.format_exc()
            logger.error("error:" + str(e))
            logger.error("trace:" + trace)
            self.set_engine()
            self.connect = self.engine
        return self.connect

    def update_sql(self, sql) -> bool:
        connect = self.get_connect()
        result = connect.execute(sql)
        return result.rowcount > 0

    def query_sql(self, sql):
        connect = self.get_connect()
        result = connect.execute(sql).fetchall()
        return result

    def get_next_id(self, primary_key: str, table: str):
        sql = f"select max({primary_key}) from {table}"
        result = self.query_sql(sql)
        max_id = result[0][0]
        if max_id is None:
            return 1
        return max_id + 1


if __name__ == '__main__':
    conn = MysqlUtils().get_connect()
    res = conn.execute("select * from sys_user limit 1").fetchall()
    print(res)
