from dataclasses import dataclass

from di.decorator import bean
from di.ref import IdRef
from tests.app_dc.cashier import Cashier
from tests.app_dc.eatingroom import EatingRoom
from tests.app_dc.kitchen import Kitchen
from tests.app_dc.staff import Staff

'''
@bean 装饰器仅用于测试register_group. 对于register及register_file无影响
'''


@bean(id="rest", refs={"manager": IdRef("manager-staff")}, group="dc")
@dataclass
class Restaurant:
    manager: Staff
    kitchen: Kitchen
    eatingroom: EatingRoom
    cashier: Cashier
