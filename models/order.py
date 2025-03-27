from types_descriptors.positive_float import PositiveFloat
from models.status import Status


class Order:
    price_purchase = PositiveFloat(True)
    price_selling = PositiveFloat(True)
    charges = PositiveFloat(True)

    def __init__(self, status:Status):
        self.price_purchase = None
        self.price_selling = None
        self.charges = None
        self.status:Status = status

    def __repr__(self):
        return f"""Order
Status:{self.status}
Price purchase:{self.price_purchase}
Price selling:{self.price_selling}
charges:{self.charges}"""
