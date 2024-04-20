from src.utils import string_utils


def trans_num(obj) -> float:
    if isinstance(obj, float):
        return obj
    if isinstance(obj, int):
        return obj
    if isinstance(obj, str):
        if string_utils.is_empty(obj):
            return 0
        else:
            try:
                return float(obj)
            except:
                return 0
    return obj
