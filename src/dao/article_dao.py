from src.dao.SingleUtils import SingleUtils
from src.entity.Article import Article
from src.utils import string_utils, common_utils
from src.utils.loging_utils import logger


def select_article_by_condition(article: Article, limit: int = None) -> list:
    sql = "select * from article"
    where_sql = common_utils.get_where_sql(article, like_list=['article_content'])
    if not string_utils.is_empty(where_sql):
        sql += " where " + where_sql
    sql += " order by article_time desc"
    if limit is not None:
        sql += f" limit {limit}"
    logger.info("sql:" + sql)
    return trans_result(sql)


def add_article(article: Article) -> bool:
    article.article_id = SingleUtils.mysql_utils.get_next_id("article_id", "article")
    entity_dict = article.__dict__
    key_str, value_str = string_utils.join_dict_list(entity_dict)
    sql = f"insert into article ({key_str}) values ({value_str})"
    logger.info("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def update_article_by_id(article: Article) -> bool:
    if article.article_id is None:
        return False
    value_str = string_utils.join_dict(article.__dict__)
    sql = f"update article set {value_str} where article_id = '{article.article_id}'"
    logger.info("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def delete_article_by_id(article_id: int) -> bool:
    sql = f"delete from article where article_id ={article_id}"
    logger.info("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def trans_result(sql: str) -> list:
    temp_dict = Article().__dict__
    conn = SingleUtils.mysql_utils.get_connect()
    result = conn.execute(sql).columns(*temp_dict.keys())
    user_list = []
    for temp in result:
        user_list.append(Article(*temp))
    return user_list


if __name__ == '__main__':
    # delete_article_by_id(84)
    res = select_article_by_condition(Article(user='chenhanwu'))
    common_utils.print_obj_list(res)
    add_article(Article(None, "chenhanwu", "adkaskosdahhhhhhxxxxxx", "../../data/test.png"))
