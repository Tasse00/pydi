from di.decorator import bean


@bean
class Seat:
    def __init__(self, id: str = "default-seat"):
        self.id = id
