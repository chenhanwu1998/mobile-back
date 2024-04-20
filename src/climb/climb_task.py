import datetime
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

from src import constant
from src.climb.evaluate_param import MobileParamEvaluate
from src.climb.mobile_company import MobileType
from src.climb.zgc_mobile import ZgcMobile
from src.service import mobile_company_service, mobile_detail_service
from src.utils.loging_utils import logger

data_path = constant.mobile_type_data_path

# 主爬虫线程池
thread_pool = ThreadPoolExecutor(max_workers=constant.THREAD_CORE_NUM)


def climb_mobile_company():
    mobile_company = MobileType()
    data_df = mobile_company.climb_mobile_type()
    mobile_company_service.save_or_update(data_df)


# 获取mobile基础信息
def climb_mobile_basic_info():
    data = pd.read_csv(data_path)
    brand_list = data['品牌']
    mobile_url_list = data['url']
    future_list = []
    for i, brand in enumerate(brand_list):
        mobile_url = mobile_url_list[i]
        zgc_mobile = ZgcMobile(brand, mobile_url)
        future_list.append(thread_pool.submit(zgc_mobile.run_cell))
        # break
    for future in as_completed(future_list):
        try:
            mobile_detail_list = future.result()
            mobile_detail_service.save_or_update(mobile_detail_list)
        except Exception as exc:
            logger.error(f"基础信息获取线程异常: {exc}")
            traceback.print_exc()


# 获取评分参数等信息
def climb_evaluate_param():
    data = pd.read_csv(data_path)
    brand_list = data['品牌']
    future_list = []
    index = 0
    for brand in brand_list:
        mobile_param_eva = MobileParamEvaluate(brand)
        future_list.append(thread_pool.submit(mobile_param_eva.run_cell))
        index += 1
        # if index == 3:
        #     break

    for future in as_completed(future_list):
        try:
            mobile_detail_list = future.result()
            mobile_detail_service.save_or_update(mobile_detail_list)
        except Exception as exc:
            logger.error(f"基础信息获取线程异常: {exc}")
            traceback.print_exc()


def climb():
    start = datetime.datetime.now()
    logger.info("爬虫任务开始")
    climb_mobile_company()
    climb_mobile_basic_info()
    climb_evaluate_param()
    logger.info("爬虫任务结束")
    end = datetime.datetime.now()
    delta = end - start
    logger.info("耗时:" + str(delta.seconds) + "s")


if __name__ == '__main__':
    climb()
