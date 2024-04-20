import pandas as pd

from src.dao import mobile_company_dao
from src.entity.MobileCompany import MobileCompany


def select_mobile_company_by_condition(company: MobileCompany, order_col: str = None,
                                       limit: int = None) -> list[MobileCompany]:
    return mobile_company_dao.select_mobile_company_by_condition(company, order_col, limit)


def save_or_update(data_df: pd.DataFrame) -> bool:
    matrix = data_df.values
    all_company = select_mobile_company_by_condition(MobileCompany())
    company_brand_list = [temp.brand for temp in all_company]
    update_company_list = []
    add_company_list = []
    for line in matrix:
        mobile_company = MobileCompany(*line)
        if mobile_company.brand not in company_brand_list:
            add_company_list.append(mobile_company)
        else:
            update_company_list.append(mobile_company)
    if len(add_company_list) != 0:
        mobile_company_dao.add_batch(add_company_list)
    if len(update_company_list) != 0:
        mobile_company_dao.update_batch(update_company_list)
    return True
