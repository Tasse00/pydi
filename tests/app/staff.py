from di.decorator import bean


@bean(id='manager-staff', consts={'name': 'manager-staff'})
@bean(id='eatingroom-staff', consts={'name': 'eatingroom-staff'})
@bean(id='kitchen-staff', consts={'name': 'kitchen-staff'})
class Staff:
    def __init__(self, name: str = "Manager"):
        self.name = name
