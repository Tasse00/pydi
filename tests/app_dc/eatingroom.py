from dataclasses import dataclass

from di.decorator import bean
from di.ref import IdRef
from tests.app_dc.seat import Seat
from tests.app_dc.staff import Staff


@bean(refs={'staff': IdRef('eatingroom-staff')}, group="dc")
@dataclass
class EatingRoom:
    staff: Staff
    seat: Seat
    # @TODO properties中的list好了后，可以将staff及seat修改为 List

