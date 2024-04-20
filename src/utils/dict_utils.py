def get_value(data: dict, key: str):
    if key in data.keys():
        return data[key]
    return None


def remove(data: dict, key: str):
    if key in data.keys():
        return data.pop(key)
    return None
