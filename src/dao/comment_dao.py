from src.dao.SingleUtils import SingleUtils
from src.entity.Comment import Comment
from src.utils import string_utils, common_utils


def select_comment_by_condition(comment: Comment) -> list:
    sql = "select * from comment"
    where_sql = common_utils.get_where_sql(comment)
    if not string_utils.is_empty(where_sql):
        sql += " where " + where_sql
    print("sql,", sql)
    return trans_result(sql)


def add_comment(comment: Comment) -> bool:
    comment.comment_id = SingleUtils.mysql_utils.get_next_id("comment_id", "comment")
    entity_dict = comment.__dict__
    key_str, value_str = string_utils.join_dict_list(entity_dict)
    sql = f"insert into comment ({key_str}) values ({value_str})"
    print("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def update_article_by_id(comment: Comment) -> bool:
    if comment.comment_id is None:
        return False
    value_str = string_utils.join_dict(comment.__dict__)
    sql = f"update comment set {value_str} where comment_id = '{comment.comment_id}'"
    print("sql:" + sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def delete_comment_by_id(comment_id: int) -> bool:
    sql = f"delete from comment where comment_id ={comment_id}"
    print("sql:", sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def delete_comment_by_article_id(article_id: int) -> bool:
    sql = f"delete from comment where article_id ={article_id}"
    print("sql:", sql)
    return SingleUtils.mysql_utils.update_sql(sql)


def trans_result(sql: str) -> list:
    temp_dict = Comment().__dict__
    conn = SingleUtils.mysql_utils.get_connect()
    result = conn.execute(sql).columns(*temp_dict.keys())
    user_list = []
    for temp in result:
        user_list.append(Comment(*temp))
    return user_list


if __name__ == '__main__':
    add_comment(Comment(None, "ggggg", "chenhanwu", 61))
    # update_article_by_id(Comment(62, "xxxxxx"))
    # delete_comment_by_id(62)
    # delete_comment_by_article_id(2)
    res = select_comment_by_condition(Comment(user="chenhanwu"))
    common_utils.print_obj_list(res)
