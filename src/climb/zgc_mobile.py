import re
import time
import traceback

import numpy as np
import pandas as pd
import requests
from lxml import etree

from src import constant
from src.entity.MobileDetail import MobileDetail
from src.utils import common_utils
from src.utils.loging_utils import logger

mobile_data_path = constant.mobile_data_path
header = constant.header


class ZgcMobile:

    def __init__(self, brand, mobile_url):
        self.detail_root = 'http://detail.zol.com.cn'  # 用来拼接成完整的链接的
        self.brand = brand
        self.mobile_url = mobile_url
        self.m_url_list = []
        self.m_id_list = []
        self.m_type_list = []
        self.m_ref_price_list = []
        self.m_descript_list = []
        self.m_score_list = []
        self.mobile_com = []
        self.review_url = []
        self.phone_img_url = []
        self.review_count = []
        self.current_len = 0

    def get_mobile_id(self, m_url_list):
        pattern = 'index(.*?)\.shtml'
        for m in m_url_list:
            id_ = re.findall(re.compile(pattern=pattern), m)
            self.m_id_list.append(id_[0])

    def get_mobile_type(self, html):
        t_pattern = "//ul[@id='J_PicMode']//h3/a"
        type_list = html.xpath(t_pattern)
        for t in type_list:
            self.m_type_list.append(t.text)
        self.current_len = len(type_list)

    def get_mobile_reference_price(self, html):
        r_pattern = "//ul[@id='J_PicMode']//div[@class='price-row']//b[@class='price-type']"
        ref_price_list = html.xpath(r_pattern)
        for r in ref_price_list:
            r = r.text.replace('即将上市', '0').replace('价格面议', '0')
            r = r.replace('概念产品', '0').replace('停产', '0')
            self.m_ref_price_list.append(r)

    def get_mobile_descript(self, html):
        d_pattern = "//ul[@id='J_PicMode']//h3/a/span"
        des_list = html.xpath(d_pattern)
        for des in des_list:
            self.m_descript_list.append(des.text)

    def get_mobile_review_url(self, html):
        for i in range(1, self.current_len + 1):
            d_pattern = f"//ul[@id='J_PicMode']/li[{i}]/div[@class='comment-row']/a[@class='comment-num']/@href"
            des_list = html.xpath(d_pattern)
            if des_list is not None and len(des_list) != 0:
                self.review_url.append(self.detail_root + des_list[0])
            else:
                self.review_url.append("")

    def get_mobile_review_count(self, html):
        pattern = '\\d+'
        for i in range(1, self.current_len + 1):
            d_pattern = f"//ul[@id='J_PicMode']/li[{i}]/div[@class='comment-row']/a[@class='comment-num']"
            des_list = html.xpath(d_pattern)
            if des_list is not None and len(des_list) != 0:
                result = re.findall(re.compile(pattern), des_list[0].text)
                if len(result) != 0:
                    self.review_count.append(result[0])
                else:
                    self.review_count.append("0")
            else:
                self.review_count.append("0")

    def run_cell(self) -> list[MobileDetail]:
        logger.info('climb:' + self.brand)
        for t in range(1, 20):  # 模拟翻页    模拟多次翻页，知道最终匹配不到错误跳出遍历
            m_url = self.mobile_url.replace('.html', f'_0_1_2_0_{t}.html')
            logger.debug('climb:' + m_url)
            try:
                page = requests.get(m_url, headers=header).text
                time.sleep(0.5)
                html = etree.HTML(page)
                m_pattern = "//ul[@id='J_PicMode']//h3/a/@href"  # 获取各个手机对应的详细信息的url
                mobile_list = html.xpath(m_pattern)
                for m in mobile_list:
                    self.m_url_list.append(self.detail_root + m)  # 将url拼接成可以访问的url

                if mobile_list is None or len(mobile_list) == 0:  # 如果爬取到的url为空的话说明没有没有这一页了，就停止翻页
                    break

                self.get_mobile_type(html)  # 手机型号
                self.get_mobile_reference_price(html)  # 参考价格
                self.get_mobile_descript(html)  # 对手机的描述
                self.get_mobile_review_url(html)
                self.get_mobile_review_count(html)

            except Exception as e:
                logger.error("e:" + str(traceback.format_exc()))
                logger.debug('没有手机啦，退出翻页!!!')
                break
            if constant.IS_TEST:
                break

        self.get_mobile_id(self.m_url_list)  # 手机id
        self.mobile_com = [self.brand] * len(self.m_id_list)

        logger.debug(len(self.m_id_list))
        logger.debug(len(self.m_type_list))
        logger.debug(len(self.m_ref_price_list))
        logger.debug(len(self.m_descript_list))
        logger.debug(len(self.m_url_list))
        logger.debug(len(self.mobile_com))
        logger.debug(len(self.review_url))
        logger.debug(len(self.review_count))

        df = pd.DataFrame({
            'id': self.m_id_list,
            'type': self.m_type_list,
            'reference_price': self.m_ref_price_list,
            'descript': self.m_descript_list,
            'url': self.m_url_list,
            'company': self.mobile_com,
            'review_url': self.review_url,
            'review_count': self.review_count,
        })

        df.to_csv(mobile_data_path + '/' + self.brand.strip() + '.csv', index=False)
        logger.info('finish climb:' + self.brand)

        self.m_url_list.clear()
        self.m_id_list.clear()
        self.m_type_list.clear()
        self.m_ref_price_list.clear()
        self.m_descript_list.clear()
        self.mobile_com.clear()
        self.review_count.clear()
        self.review_url.clear()

        source_col = ["id", "type", "reference_price", "descript", "descript", "company", "review_url", "review_count",
                      "url"]
        target_col = ["id", "type", "reference_price", "descript", "descript", "company_type", "evaluate_url",
                      "review_count", "url"]
        target_df = df[source_col]
        mobile_detail_list = []
        for line in target_df.values:
            mobile_detail = MobileDetail(**dict(zip(target_col, list(line))))
            mobile_detail_list.append(mobile_detail)
        return mobile_detail_list


if __name__ == '__main__':
    data = [
        [1, 2, 4],
        [3, 4, 0]
    ]
    data_df = pd.DataFrame(np.array(data), columns=["type", "id", "descript"])
    cols = ["type", "id", "descript"]
    temp_list = []
    for temp_line in data_df.values:
        temp_mobile = MobileDetail(**dict(zip(cols, list(temp_line))))
        temp_list.append(temp_mobile)
    common_utils.print_obj_list(temp_list)
