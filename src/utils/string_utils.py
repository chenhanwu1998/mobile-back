def join(str_list: list, trans_str=False, sep: str = ",") -> str:
    index = 0
    length = len(str_list)
    result = ""
    for temp in str_list:
        if temp is None:
            temp = ""
        if isinstance(temp, int) or isinstance(temp, float):
            temp = str(temp)
        elif isinstance(temp, str):
            if trans_str:
                temp = f"'{temp}'"
        else:
            temp = f"'{temp}'"
        result += temp
        if index != length - 1:
            result += " " + sep + " "
        index += 1

    result = result.strip().strip(sep)
    return result


def join_obj_value_list(data_list: list) -> str:
    value_list = []
    for temp in data_list:
        temp_dict = temp.__dict__
        temp_value_str = join(list(temp_dict.values()), True)
        value_list.append(f"({temp_value_str})")
    return join(value_list, False)


def join_dict_list(data_dict: dict) -> tuple[str, str]:
    key_list = []
    value_list = []
    for k, v in data_dict.items():
        if v is None:
            continue
        key_list.append(k)
        value_list.append(v)
    return join(key_list, False), join(value_list, True)


def join_dict(data_dict: dict, trans_str: bool = True) -> str:
    str_list = []
    for k, v in data_dict.items():
        if (isinstance(v, int) or isinstance(v, float)) and v == 0:
            continue
        if v is None:
            continue
        if trans_str:
            v = f"'{v}'"
        str_list.append(f"{k}={v}")
    return join(str_list, False)


def is_empty(string: str):
    if not isinstance(string, str):
        return False
    if string is None:
        return True
    if len(string.strip()) == 0:
        return True
    return False
