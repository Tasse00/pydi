from dataclasses import dataclass

from di.decorator import bean


@bean(group="dc")
@dataclass
class Seat:
    id: str = "default-seat"

