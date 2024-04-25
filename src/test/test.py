import base64
import re
from random import  Random


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
    for i in range(100):
        rand = Random().randint(1, 5)
        print(rand)
    pass
