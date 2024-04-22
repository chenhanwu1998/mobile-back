from src.dao import article_dao, comment_dao
from src.dto import ArticleDTO
from src.entity.Article import Article
from src.utils import convert_utils


def select_article_by_condition(article: Article, limit: int = None) -> list[ArticleDTO]:
    article_list = article_dao.select_article_by_condition(article, limit)
    article_id_list = []
    for article in article_list:
        article_id_list.append(article.article_id)
    comment_list = comment_dao.select_comment_by_article_id_list(article_id_list)
    comment_dict = dict()
    for comment in comment_list:
        if comment.article_id not in comment_dict.keys():
            comment_dict[comment.article_id] = []
        comment_dict[comment.article_id].append(comment)
    article_dto_list = []
    for article in article_list:
        article_dto = convert_utils.convert_article_to_dto(article)
        if article.article_id in comment_dict.keys():
            article_dto.comment_list = comment_dict[article.article_id]
        article_dto_list.append(article_dto)
    return article_dto_list


def add_article(article: Article) -> bool:
    return article_dao.add_article(article)


def update_article_by_id(article: Article) -> bool:
    return article_dao.update_article_by_id(article)


def delete_article_by_id(article_id: int) -> bool:
    result = article_dao.delete_article_by_id(article_id)
    comment_dao.delete_comment_by_article_id(article_id)
    return result
