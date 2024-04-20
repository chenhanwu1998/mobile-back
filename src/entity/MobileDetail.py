from _datetime import datetime

from src.utils.number_utils import trans_num


class MobileDetail:
    def __init__(self, cpu: str = None, id: int = None, param_url: str = None, market_date: str = None,
                 resolution: str = None, screen_size: str = None, internal_storage: str = None, font_camera: str = None,
                 rear_camera: str = None, kernel_count: str = None, battery_capacity: str = None,
                 battery_type: str = None, cost_performance: float = 0, performance: float = 0,
                 continuation: float = 0, appearance: float = 0, photograph: float = 0,
                 four_five_star: str = None, three_four_star: str = None, two_three_star: str = None,
                 one_two_star: str = None, score: float = 0, descript: str = None, evaluate_url: str = None,
                 detail_descript: str = None, reference_price: float = 0, type: str = None, url: str = None,
                 review_count: int = 0, img_url: str = None, company_type: str = None,
                 update_time: datetime = datetime.now()):
        self.cpu = cpu
        self.id = id
        self.param_url = param_url
        self.market_date = market_date
        self.resolution = resolution
        self.screen_size = screen_size
        self.internal_storage = internal_storage
        self.font_camera = font_camera
        self.rear_camera = rear_camera
        self.kernel_count = kernel_count
        self.battery_capacity = battery_capacity
        self.battery_type = battery_type
        self.cost_performance = trans_num(cost_performance)
        self.performance = trans_num(performance)
        self.continuation = trans_num(continuation)
        self.appearance = trans_num(appearance)
        self.photograph = trans_num(photograph)
        self.four_five_star = four_five_star
        self.three_four_star = three_four_star
        self.two_three_star = two_three_star
        self.one_two_star = one_two_star
        self.score = trans_num(score)
        self.descript = descript
        self.evaluate_url = evaluate_url
        self.detail_descript = detail_descript
        self.reference_price = trans_num(reference_price)
        self.type = type
        self.url = url
        self.review_count = trans_num(review_count)
        self.img_url = img_url
        self.company_type = company_type
        self.update_time = update_time
