import re
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd
import requests
from lxml import etree

from src import constant
from src.entity.MobileDetail import MobileDetail
from src.utils.loging_utils import logger

data_path = constant.mobile_type_data_path
mobile_data_path = constant.mobile_data_path
param_data_path = constant.param_data_path
evaluate_data_path = constant.evaluate_data_path
header = constant.header

# 子爬虫线程池
second_thread_pool = ThreadPoolExecutor(max_workers=constant.SECOND_THREAD_CORE_NUM)


class MobileParam:
    def __init__(self):
        self.params_dic = {'id': [], 'cpu': [], '上市日期': [], '主屏尺寸': [], '主屏分辨率': [], '后置摄像头': [],
                           '前置摄像头': [], '电池容量': [], '电池类型': [],
                           '核心数': [], '内存': [], 'param_url': [], 'img_url': []}
        self.evaluate_dic = {'id': [], '性价比': [], '性能': [], '续航': [], '外观': [], '拍照': [], '4-5星': [],
                             '3-4星': [], '2-3星': [],
                             '1-2星': [], 'score': [], 'descript': [], 'evaluate_url': []}
        self.temp_params_dic = {'id': 'None', 'cpu': 'None', '上市日期': 'None', '主屏尺寸': 'None',
                                '主屏分辨率': 'None', '后置摄像头': 'None', '前置摄像头': 'None',
                                '电池容量': 'None', '电池类型': 'None',
                                '核心数': 'None', '内存': 'None', 'param_url': 'None', 'img_url': 'None'}
        self.temp_evaluate_dic = {'id': 'None', '性价比': 'None', '性能': 'None', '续航': 'None', '外观': 'None',
                                  '拍照': 'None', '4-5星': 'None', '3-4星': 'None',
                                  '2-3星': 'None',
                                  '1-2星': 'None', 'score': 'None', 'descript': 'None', 'evaluate_url': 'None'}


class MobileParamEvaluate:
    def __init__(self, brand):
        self.brand = brand.strip()
        self.detail_root = 'http://detail.zol.com.cn'

        self.count = 0
        self.all_count = 0
        self.mobile_param = MobileParam()

    def get_page(self, url):
        # proxies = {
        #     "http": "http://10.10.1.10:3128",
        #     "https": "http://10.10.1.10:1080",
        # }
        # response = requests.get("http://example.org", proxies=proxies)
        while True:
            try:
                param_page = requests.get(url, headers=header).text
                return param_page
            except Exception as e:
                logger.error(f"请求错误:{e},url:{url}")
                # traceback.print_exc()

    def get_mobile_param(self, param_url, temp_params_dic):
        # 获取手机的上市日期和CPU型号，顺便做了简单初步去噪
        logger.debug('climb param:' + param_url)
        temp_params_dic['param_url'] = param_url

        param_page = self.get_page(param_url)  # 参数url
        time.sleep(0.5)
        param_html = etree.HTML(param_page)

        date_pattern = "//span[@id='newPmVal_1']"
        an_dt_pattern = date_pattern + "/a"
        label = "//span[@id='newPmName_1']"
        dt = param_html.xpath(date_pattern)
        an_dt = param_html.xpath(an_dt_pattern)
        lab = param_html.xpath(label)

        temp_date = 'None'
        if lab and len(lab) >= 2 and lab[1].text == '上市日期':
            if dt and dt[1].text:
                temp_date = dt[1].text
            elif an_dt:
                temp_date = an_dt[1].text.replace('>', '')

        temp_params_dic['上市日期'] = temp_date

        pt = "//div[@class='wrapper clearfix mt30']//div[@class='box-item-fl ']"
        label = pt + "//label[@class='name']"
        an_pt = "//span[@id='newPmVal_3']"
        xinhao = "//a[@id='newPmName_3']"
        lab = param_html.xpath(label)
        cpu_con = param_html.xpath(pt)
        an_cpu_con = param_html.xpath(an_pt)
        xinhao = param_html.xpath(xinhao)

        temp_cpu = 'None'
        if cpu_con:
            if lab[0].text == 'CPU：':
                cpu_con = param_html.xpath(pt)[0].xpath('string(.)')
                cpu_con = cpu_con.replace('\t', '').replace('\r', '').replace(' ', '')
                cpu_list = [t for t in cpu_con.split('\n') if len(t) != 0]
                temp_cpu = cpu_list[0].split('：')[1].split('游戏')[0].split('手机')[0]
        elif an_cpu_con:
            if xinhao and xinhao[0].text == 'CPU型号':
                an_cpu_con = an_cpu_con[0].xpath('string(.)')
                cpu = an_cpu_con.split('更多')[0]
                cpu = cpu.split('手机')[0]
                temp_cpu = cpu.split('游戏')[0]
        temp_params_dic['cpu'] = temp_cpu
        if temp_params_dic['img_url'] is None:
            img_url_list = param_html.xpath("//div[@class='wrapper clearfix mt30']/div[@class='big-pic-fl']/a/img/@src")
            if img_url_list is not None and len(img_url_list) != 0:
                temp_params_dic['img_url'] = img_url_list[0]

        # an_zp_th_pattern = f'//div[@class="detailed-parameters"]//table//tr/th/span'
        # an_zp_td_pattern = f'//div[@class="detailed-parameters"]//table//tr/td[@class="hover-edit-param "]'
        # th_list = param_html.xpath(an_zp_th_pattern)
        # td_list = param_html.xpath(an_zp_td_pattern)
        # print(len(th_list))
        # print(len(td_list))
        # print(th_list[0].text, ":", td_list[0].xpath("string(.)"))

    def get_mobile_detail_param(self, html, temp_params_dic):
        zp_pattern = "//div[@class='wrapper clearfix']//ul[@class='product-param-item pi-57 clearfix']//li"
        key_list = ['主屏尺寸', '主屏分辨率', '后置摄像头', '前置摄像头', '电池容量', '电池类型', '核心数', '内存']
        param = html.xpath(zp_pattern)
        if len(param) != 0:  # 样式还是老版的情况下的爬虫
            params = ''
            for pa in param:
                params += pa.xpath('string(.)').replace('\t', '').replace('\r', '')
            p_list = params.split('\n')
            real_p = [r for r in p_list if len(r) != 0]

            temp_dic = {}  # 先用字典缓存起来
            for r in real_p:
                r_cell = r.split('：')
                try:  # 在此可能有其他杂质出现try一下
                    temp_dic[r_cell[0]] = r_cell[1]
                except:
                    pass

            for key in key_list:  # 将缓存写入类字典中去
                if key in temp_dic.keys():
                    temp_params_dic[key] = temp_dic[key]
                else:
                    temp_params_dic[key] = 'None'

        else:  # 新样式爬虫，网站样式排版改变后，再加上另外一种分析机制
            zp_pattern = '//*[@id="secondsUnderstand"]//div[@class="tab-con"]//div[@class="info-list-01"]//ul'
            key_list1 = ['屏幕', '分辨率', '后置', '前置', '电池', '内存']
            key_list2 = ['主屏尺寸', '主屏分辨率', '后置摄像头', '前置摄像头', '电池容量', '内存']
            param = html.xpath(zp_pattern)
            if param is None or len(param) == 0:  # 判断是否存在先
                return
            param = param[0]
            param = param.xpath('string(.)').replace('\t', '').replace('\r', '').replace(' ', '')  # 获取所有的在这个标签内的东西后再做分割
            param_list = param.split('\n')
            param_list = [p for p in param_list if len(p) != 0 and '：' in p]  # 顺便去掉一些噪音字符
            temp_param = {}
            for temp_p in param_list:
                cell = temp_p.split('：')
                if cell[0] in key_list1:
                    temp_param[cell[0]] = cell[1]

            for i, key in enumerate(key_list1):  # 可能有些情况下爬取不到分辨率等这些，需要做个判断然后置none ，血腥报错
                if key in temp_param.keys():
                    temp_params_dic[key_list2[i]] = temp_param[key]
                else:
                    temp_params_dic[key_list2[i]] = 'None'

            for key in key_list:  # 对params_dic中的key没有在keylist2中的参数置为none
                if key not in key_list2:
                    temp_params_dic[key] = 'None'

    def get_eva_score(self, html, temp_evaluate_dic):
        # 获取评价指标，将指标写入字典中存储
        eva_v_pattern = "//div[@class='total-bd clearfix']//div[@class='circle-value']"
        eva_t_pattern = "//div[@class='total-bd clearfix']//div[@class='circle-text']"
        eva_v_list = html.xpath(eva_v_pattern)
        eva_t_list = html.xpath(eva_t_pattern)
        eva_value_list = ['None', 'None', 'None', 'None', 'None']
        eva_text_list = ['性价比', '性能', '续航', '外观', '拍照']
        eva_dic = dict(zip(eva_text_list, eva_value_list))

        for i, eva_t in enumerate(eva_t_list):
            try:
                eva_dic[eva_t.text] = eva_v_list[i].text
            except:
                break

        for k, v in eva_dic.items():
            temp_evaluate_dic[k] = v

    def get_score(self, html, temp_evaluate_dic):
        # 获取得分
        eva_s_pattern = "//div[@class='total-bd clearfix']//div[@class='total-score']/strong"
        eva_score = html.xpath(eva_s_pattern)
        if eva_score:
            temp_evaluate_dic['score'] = eva_score[0].text

    def get_descript(self, html, temp_evaluate_dic):
        # 获取手机的相关描述
        peo_d_pattern = "//ul[@id='_j_words_filter']//a"
        peo_des_list = html.xpath(peo_d_pattern)
        peo_descript_list = []
        for peo_d in peo_des_list:
            peo_descript_list.append(peo_d.text)
        if peo_des_list:  # 存在的话
            temp_evaluate_dic['descript'] = '、'.join(peo_descript_list)

    def get_mobile_evaluate(self, evaluate_url, temp_evaluate_dic):
        logger.debug('climb evaluate:' + evaluate_url)
        temp_evaluate_dic['evaluate_url'] = evaluate_url
        evaluate_page = self.get_page(evaluate_url)  # 评论url
        time.sleep(0.5)
        html = etree.HTML(evaluate_page)
        self.get_eva_score(html, temp_evaluate_dic)
        self.get_score(html, temp_evaluate_dic)
        self.get_descript(html, temp_evaluate_dic)

    def get_mobile_id(self, m_url, temp_params_dic, temp_evaluate_dic):
        pattern = 'index(.*?)\.shtml'
        id_ = re.findall(re.compile(pattern=pattern), m_url)
        temp_params_dic['id'] = id_[0]
        temp_evaluate_dic['id'] = id_[0]

    def check_dic(self, params_dic, evaluate_dic):
        # 输出一下长度做检查
        for k in evaluate_dic.keys():
            print(k, ":", len(evaluate_dic[k]))
        for k in params_dic.keys():
            print(k, ":", len(params_dic[k]))

    def clear_dic(self, params_dic, evaluate_dic):
        # 将主字典清空
        for k in params_dic.keys():
            params_dic[k].clear()
        for k in evaluate_dic.keys():
            evaluate_dic[k].clear()

    def clear_temp_dic(self, temp_params_dic, temp_evaluate_dic):
        # 将临时字典清空
        for k in temp_params_dic.keys():
            temp_params_dic[k] = 'None'
        for k in temp_evaluate_dic.keys():
            temp_evaluate_dic[k] = 'None'

    def run_little_cell(self, mobile_param: MobileParam, sub_mobile_list) -> MobileParam:
        temp_params_dic = mobile_param.temp_params_dic
        temp_evaluate_dic = mobile_param.temp_evaluate_dic
        params_dic = mobile_param.params_dic
        evaluate_dic = mobile_param.evaluate_dic
        for i, m_url in enumerate(sub_mobile_list):
            logger.debug('climb ' + m_url)

            page = self.get_page(m_url)
            html = etree.HTML(page)  # 综述页面

            pattern = "//div[@id='_j_tag_nav']/ul/li[4]/a/@href"
            temp_url = html.xpath(pattern)  # 获取参数的链接
            if temp_url is not None and len(temp_url) != 0:  # 如果有此链接，才调到此处继续，否则直接跳过所有一下操作
                temp_url = temp_url[0]  # 如果有就取出第一个
            else:
                continue
            pattern = "//div[@class='product-pics']/div[@class='big-pic']/a/img/@src"
            img_url_list = html.xpath(pattern)
            # logger.info("img_url_list:" + str(img_url_list))
            if img_url_list is not None and len(img_url_list) != 0:
                temp_params_dic["img_url"] = img_url_list[0]

            find_patten = '/(\d+/\d+).*shtml'
            real_url_id = re.findall(find_patten, temp_url)[0]
            param_url = self.detail_root + '/' + real_url_id + '/param.shtml'
            evaluate_url = self.detail_root + '/' + real_url_id + '/review.shtml'

            self.get_mobile_id(m_url, temp_params_dic, temp_evaluate_dic)  # 获取id
            self.get_mobile_detail_param(html, temp_params_dic)
            self.get_mobile_param(param_url, temp_params_dic)
            self.get_mobile_evaluate(evaluate_url, temp_evaluate_dic)

            for k, v in temp_params_dic.items():
                params_dic[k].append(v)
            for k, v in temp_evaluate_dic.items():
                evaluate_dic[k].append(v)

            logger.debug(temp_params_dic)
            logger.debug(temp_evaluate_dic)
            self.clear_temp_dic(temp_params_dic, temp_evaluate_dic)  # 清楚临时字典

            self.count += 1
            if self.count == self.all_count or self.count % 10 == 0:
                logger.info(
                    f"brand:{self.brand},count:{self.count}/{self.all_count},进度:{round(self.count / self.all_count, 4) * 100}%")
            if constant.IS_TEST and self.count == 10:
                break
        return mobile_param

    def run_cell(self) -> list[MobileDetail]:
        d_path = mobile_data_path + '/' + self.brand + '.csv'
        logger.info('climb:' + self.brand + "  d_path:" + d_path)

        data_df = pd.read_csv(d_path)
        mobile_url_list = data_df['url']
        self.all_count = len(mobile_url_list)
        start_index = 0
        sep = 20
        end_index = start_index + sep
        future_list = []
        while start_index <= self.all_count:
            if end_index > self.all_count:
                end_index = self.all_count
            sub_list = mobile_url_list[start_index:end_index]
            if sub_list is None or len(sub_list) == 0:
                break
            mobile_param = MobileParam()
            future_list.append(second_thread_pool.submit(self.run_little_cell, mobile_param, sub_list))
            start_index = start_index + sep
            end_index = start_index + sep

        param_df = None
        evaluate_df = None
        for future in as_completed(future_list):
            try:
                mobile_param = future.result()
                temp_param_df = pd.DataFrame(mobile_param.params_dic)  # 装成pandas数据模式
                temp_evaluate_df = pd.DataFrame(mobile_param.evaluate_dic)
                if param_df is None:
                    param_df = temp_param_df
                else:
                    param_df = pd.concat([param_df, temp_param_df], axis=0)
                if evaluate_df is None:
                    evaluate_df = temp_evaluate_df
                else:
                    evaluate_df = pd.concat([evaluate_df, temp_evaluate_df], axis=0)
                self.clear_dic(mobile_param.params_dic, mobile_param.evaluate_dic)  # 清掉词典
            except Exception as exc:
                logger.error(f"基础信息获取线程异常: {exc}")
                traceback.print_exc()

        # self.check_dic()  #输出检查一下具体字典的长度
        param_data_to_path = param_data_path + '/param_' + self.brand + '.csv'
        evaluate_data_to_path = evaluate_data_path + '/evaluate_' + self.brand + '.csv'

        if param_df is None or evaluate_df is None:
            logger.error(f"error csv为空,brand:{self.brand}")
            return []
        param_df.to_csv(param_data_to_path, index=False)  # 存储成csv文件
        evaluate_df.to_csv(evaluate_data_to_path, index=False)
        logger.info('finish climb:' + self.brand)

        source_params_col = ["id", "cpu", "上市日期", "主屏尺寸", "主屏分辨率", "后置摄像头", "前置摄像头",
                             "电池容量",
                             "电池类型", "核心数", "内存", "param_url", "img_url"]
        source_eva_col = ["id", "性价比", "性能", "续航", "外观", "拍照", "score", "descript", "evaluate_url"]
        target_param_df = param_df[source_params_col]
        target_eva_df = evaluate_df[source_eva_col]

        target_data_df = target_param_df.merge(target_eva_df, on="id", how="outer")
        target_all_col = ["id", "cpu", "market_date", "screen_size", "resolution", "rear_camera", "font_camera",
                          "battery_capacity", "battery_type", "kernel_count", "internal_storage", "param_url",
                          "img_url", "cost_performance", "performance", "continuation", "appearance", "photograph",
                          "score", "detail_descript", "evaluate_url"]
        # target_data_df.to_csv("../../data/mobile/test.csv", index=False)
        mobile_detail_list = []
        for line in target_data_df.values:
            mobile_detail = MobileDetail(**dict(zip(target_all_col, list(line))))
            mobile_detail_list.append(mobile_detail)
        return mobile_detail_list


if __name__ == '__main__':
    data1 = pd.DataFrame(np.array([
        [1, 2, 3],
        [2, 33, 77]
    ]), columns=["col1", "col2", "col3"])
    data2 = pd.DataFrame(np.array(
        [[1, 2, 5, 4],
         [3, 4, 5, 0]]
    ), columns=["col1", "col4", "col5", "col6"])
    print(data1)
    print(data2)
    target_df = data1.merge(data2, on="col1", how="outer")
    print(target_df)

    # all_count = 61
    # mobile_url_list_temp = ["str" + str(i) for i in range(all_count)]
    # start_index = 0
    # sep = 20
    # end_index = start_index + sep
    # future_list = []
    # while start_index <= all_count:
    #     if end_index > all_count:
    #         end_index = all_count
    #     sub_list = mobile_url_list_temp[start_index:end_index]
    #     if sub_list is None or len(sub_list) == 0:
    #         break
    #     print(sub_list)
    #     start_index = start_index + sep
    #     end_index = start_index + sep

    temp_df = None
    for i in range(5):
        data2 = pd.DataFrame(np.array(
            [[1, 2, 5, 4],
             [3, 4, 5, 0]]
        ), columns=["col1", "col4", "col5", "col6"])
        if temp_df is None:
            temp_df = data2
        else:
            temp_df = pd.concat([temp_df, data2], axis=0)
    data3 = pd.DataFrame()
    temp_df = pd.concat([temp_df, data3], axis=0)
    print(temp_df.shape)
    print(temp_df)
