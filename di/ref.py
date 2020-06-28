import abc
import enum
from typing import Union

from di.utils import get_cls_name


class RefType(str, enum.Enum):
    Id = "id"
    Cls = "cls"


class Ref(abc.ABC):

    def __init__(self, type: RefType, target: str):
        self.type = type
        self.target = target

    def __eq__(self, other):
        return self.type == other.type and self.target == other.target

    def __hash__(self):
        return hash("{}||{}".format(self.type, self.target))

    def __repr__(self):
        return "<%s:%s>" % (self.type.value, self.target)

    def to_expr(self) -> str:
        return "%s:%s" % (self.type.value, self.target)

    @classmethod
    def from_expr(cls, expr: str) -> 'Ref':
        type_val, target = expr.split(':')
        return cls(type=RefType(type_val), target=target)


class IdRef(Ref):
    def __init__(self, tgt: str):
        super(IdRef, self).__init__(RefType.Id, tgt)


class ClsRef(Ref):
    def __init__(self, tgt: Union[type, str]):
        if isinstance(tgt, type):
            tgt = get_cls_name(tgt)
        super(ClsRef, self).__init__(RefType.Cls, tgt)
