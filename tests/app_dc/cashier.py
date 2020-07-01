from dataclasses import dataclass

from di.decorator import bean
from di.ref import IdRef
from tests.app_dc.staff import Staff


@bean(refs={'staff': IdRef('manager-staff')}, group="dc")
@dataclass
class Cashier:
    staff: Staff
