import json

from sqlalchemy import create_engine

from src.constant import CONFIG_PATH, MYSQL, SQLITE


def get_config():
    file = open(CONFIG_PATH, 'r', encoding='utf-8')
    config = json.load(file)
    print("config:", config)
    return config


class MysqlUtils:

    def __init__(self):
        self.connect = None

    def get_connect(self):
        if self.connect is None:
            config = get_config()
            if config["DB_TYPE"] == MYSQL:
                self.connect = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4'
                                             % (config['MYSQL_USER'], config['MYSQL_PASSWORD'], config['MYSQL_HOST'],
                                                config['MYSQL_PORT'], config['MYSQL_DB']), )
            elif config["DB_TYPE"] == SQLITE:
                self.connect = create_engine('sqlite:///' + config["SQLITE_PATH"])
            else:
                raise Exception("数据库配置错误")
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
        return max_id + 1


if __name__ == '__main__':
    conn = MysqlUtils().get_connect()
    res = conn.execute("select * from sys_user limit 1").fetchall()
    print(res)
