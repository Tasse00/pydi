from di.decorator import bean
from di.ref import IdRef
from tests.app.staff import Staff


@bean(refs={'staff': IdRef('manager-staff')})
class Cashier:
    def __init__(self, staff: Staff):
        self.staff = staff
