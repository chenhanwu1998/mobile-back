import base64
import datetime
import re
import traceback

import requests
from lxml import etree

from src.climb.climb_task import climb
from src.constant import header
from src.dao import mobile_detail_dao
from src.entity.MobileDetail import MobileDetail


def trans_photo():
    with open("../../data/forum/photo/logo-sin.jpg", 'rb') as file:
        encode_str = base64.b64encode(file.read()).decode("utf-8")
    return encode_str


def read_py_pkg():
    file = open("../../data/test.txt", 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()
    cell_list = []
    for line in lines:
        cells = re.split(" +", line.strip())
        if "K" in cells[0]:
            cells[0] = float(cells[0].replace("K", ""))
        elif "M" in cells[0]:
            cells[0] = float(cells[0].replace("M", "")) * 1000
        print(cells)
        cell_list.append(cells)
    cell_list = sorted(cell_list, key=lambda k: k[0])
    for temp in cell_list:
        print(temp)



if __name__ == '__main__':
    # prefix = "data:image/jpg;base64,"
    # base64_img = trans_photo()
    # print(prefix + base64_img)
    # read_py_pkg()
    # for i in range(100):
    #     rand = Random().randint(1, 5)
    #     print(rand)
    # get_mobile_img()
    climb()
    pass
