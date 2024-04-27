import datetime
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

from src import constant
from src.climb.evaluate_param import MobileParamEvaluate
from src.climb.mobile_company import MobileType
from src.climb.zgc_mobile import ZgcMobile
from src.dao import mobile_detail_dao
from src.service import mobile_company_service, mobile_detail_service
from src.utils import string_utils
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
    for brand in brand_list:
        mobile_param_eva = MobileParamEvaluate(brand)
        future_list.append(thread_pool.submit(mobile_param_eva.run_cell))
        # break

    for future in as_completed(future_list):
        try:
            mobile_detail_list = future.result()
            mobile_detail_service.save_or_update(mobile_detail_list)
        except Exception as exc:
            logger.error(f"基础信息获取线程异常: {exc}")
            traceback.print_exc()


def get_single_img(mobile_param_eva, mobile):
    img_url = mobile_param_eva.get_img_url(mobile.url)
    if not string_utils.is_empty(img_url):
        mobile.img_url = img_url
        mobile.update_time = datetime.datetime.now()
        mobile_detail_dao.update_batch([mobile])
    return True


def get_mobile_img_what_is_none():
    mobile_list = mobile_detail_dao.select_mobile_url_is_null()
    mobile_param_eva = MobileParamEvaluate("获取缺失图片")
    logger.info("总共没有图片的手机数量:" + str(len(mobile_list)))
    mobile_param_eva.all_count = len(mobile_list)
    future_list = []
    for mobile in mobile_list:
        future_list.append(thread_pool.submit(get_single_img, mobile_param_eva, mobile))
        # break
    for future in as_completed(future_list):
        try:
            result = future.result()
        except Exception as exc:
            logger.error(f"基础信息获取线程异常: {exc}")
            traceback.print_exc()


def climb():
    start = datetime.datetime.now()
    logger.info("爬虫任务开始")
    # climb_mobile_company()
    # climb_mobile_basic_info()
    climb_evaluate_param()
    # get_mobile_img_what_is_none()
    logger.info("爬虫任务结束")
    end = datetime.datetime.now()
    delta = end - start
    logger.info("爬虫耗时:" + str(delta.seconds) + "s")


if __name__ == '__main__':
    climb()
