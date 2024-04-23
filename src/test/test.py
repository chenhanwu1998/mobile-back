import base64


def trans_photo():
    with open("../../data/forum/photo/logo-sin.jpg", 'rb') as file:
        encode_str = base64.b64encode(file.read()).decode("utf-8")
    return encode_str


if __name__ == '__main__':
    prefix = "data:image/jpg;base64,"
    base64_img = trans_photo()
    print(prefix + base64_img)
