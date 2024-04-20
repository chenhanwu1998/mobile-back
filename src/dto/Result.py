class Result:
    def __init__(self, code: int, msg: str, data: object):
        self.code = code
        self.msg = msg
        self.data = data

    @staticmethod
    def success(data: object):
        return Result(0, "操作成功", data)

    @staticmethod
    def fail(data: object):
        return Result(-1, "操作失败", data)

    @staticmethod
    def fail_401(data: object):
        return Result(401, "操作失败", data)
