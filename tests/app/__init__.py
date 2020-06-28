from di.decorator import bean
from di.ref import IdRef
from tests.app.cashier import Cashier
from tests.app.eatingroom import EatingRoom
from tests.app.kitchen import Kitchen
from tests.app.staff import Staff

'''
@bean 装饰器仅用于测试register_group. 对于register及register_file无影响
'''


@bean(id="rest", refs={"manager": IdRef("manager-staff")})
class Restaurant:
    def __init__(self,
                 manager: Staff, kitchen: Kitchen,
                 eatingroom: EatingRoom, cashier: Cashier):
        self.manager = manager
        self.kitchen = kitchen
        self.eatingroom = eatingroom
        self.cashier = cashier
