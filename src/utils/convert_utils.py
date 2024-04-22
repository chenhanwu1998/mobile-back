from src.dto.ArticleDTO import ArticleDTO
from src.dto.SysUserDTO import SysUserDTO
from src.entity.Article import Article
from src.entity.SysUser import SysUser


def convert_user(user: SysUser) -> SysUserDTO:
    user_dto = SysUserDTO(**user.__dict__)
    return user_dto


def convert_article_to_dto(article: Article) -> ArticleDTO:
    article_dto = ArticleDTO(**article.__dict__)
    return article_dto


def convert_dict(obj: object, data_dict: dict) -> dict:
    target_dict = obj.__dict__
    for k, v in target_dict.items():
        if k in data_dict.keys():
            target_dict[k] = data_dict[k]
    return target_dict
