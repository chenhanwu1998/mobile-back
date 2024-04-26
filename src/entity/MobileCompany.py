from datetime import datetime


class MobileCompany:
    def __init__(self, brand=None, brand_score=None, brand_occup=None, good_score=None, low_price=None, high_price=None,
                 url=None, update_time: datetime = None):
        self.brand = brand
        self.brand_score = brand_score
        self.brand_occup = brand_occup
        self.good_score = good_score
        self.low_price = low_price
        self.high_price = high_price
        self.url = url
        if update_time is None:
            self.update_time = datetime.now()
        else:
            self.update_time = update_time
