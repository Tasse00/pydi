from di.decorator import bean
from di.ref import IdRef
from tests.app.staff import Staff


@bean(refs={'staff': IdRef('kitchen-staff')})
class Kitchen:
    def __init__(self, staff: Staff, number: int = 1):
        self.staff = staff
        self.number = number
