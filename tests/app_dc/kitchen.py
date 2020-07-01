from dataclasses import dataclass

from di.decorator import bean
from di.ref import IdRef
from tests.app_dc.staff import Staff


@bean(refs={'staff': IdRef('kitchen-staff')}, group="dc")
@dataclass
class Kitchen:
    staff: Staff
    number: int = 1
