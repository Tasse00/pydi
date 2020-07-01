from dataclasses import dataclass

from di.decorator import bean


@bean(id='manager-staff', consts={'name': 'manager-staff'}, group="dc")
@bean(id='eatingroom-staff', consts={'name': 'eatingroom-staff'}, group="dc")
@bean(id='kitchen-staff', consts={'name': 'kitchen-staff'}, group="dc")
@dataclass
class Staff:
    name: str = "Manager"
