from di.decorator import bean
from di.ref import IdRef
from tests.app.seat import Seat
from tests.app.staff import Staff


@bean(refs={'staff': IdRef('eatingroom-staff')})
class EatingRoom:
    def __init__(self, staff: Staff, seat: Seat):
        # @TODO properties中的list好了后，可以将staff及seat修改为 List
        self.staff = staff
        self.seat = seat
