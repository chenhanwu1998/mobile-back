from datetime import datetime

from src.entity.MobileDetail import MobileDetail


class MobileDetailDTO(MobileDetail):
    def __init__(self, cpu: str = None, id: int = None, param_url: str = None, market_date: str = None,
                 resolution: str = None, screen_size: str = None, internal_storage: str = None, font_camera: str = None,
                 rear_camera: str = None, kernel_count: str = None, battery_capacity: str = None,
                 battery_type: str = None, cost_performance: float = 0, performance: float = 0,
                 continuation: float = 0, appearance: float = 0, photograph: float = 0,
                 four_five_star: str = None, three_four_star: str = None, two_three_star: str = None,
                 one_two_star: str = None, score: float = 0, descript: str = None, evaluate_url: str = None,
                 detail_descript: str = None, reference_price: float = 0, type: str = None, url: str = None,
                 review_count: int = 0, img_url: str = None, company_type: str = None,
                 update_time: datetime = datetime.now(), mobile_num: int = 0, cpu_num: int = 0):
        super().__init__(cpu, id, param_url, market_date,
                         resolution, screen_size, internal_storage, font_camera,
                         rear_camera, kernel_count, battery_capacity,
                         battery_type, cost_performance, performance,
                         continuation, appearance, photograph,
                         four_five_star, three_four_star, two_three_star,
                         one_two_star, score, descript, evaluate_url,
                         detail_descript, reference_price, type, url,
                         review_count, img_url, company_type,
                         update_time)
        self.mobile_num = mobile_num
        self.cpu_num = cpu_num
