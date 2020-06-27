import enum
# noinspection PyUnresolvedReferences
import xml.dom.minidom
from typing import Union, Any, List

from di.ref import Ref


class ParamType(int, enum.Enum):
    Const = 1
    Ref = 2


class Param:

    def __init__(self, name: str, type: ParamType, value: Union[Any, Ref]):
        self.name = name
        self.type = type
        self.value = value

    def to_xml(self):
        elem = xml.dom.minidom.Document().createElement('param')
        elem.setAttribute("name", self.name)
        elem.setAttribute("type", self.type.name)
        elem.setAttribute("value", str(self.value))
        return elem

    def __repr__(self):
        return self.to_xml().toxml()


class Bean:

    def __init__(self,
                 cls: str,
                 id: str,
                 singleton: bool,
                 params: List[Param]):
        self.cls = cls
        self.params = params
        self.id = id
        self.singleton = singleton

    def to_xml(self):
        bean = xml.dom.minidom.Document().createElement('bean')
        bean.setAttribute("cls", self.cls)
        bean.setAttribute("id", self.id)
        bean.setAttribute("singleton", str(self.singleton))

        for param in self.params:
            bean.appendChild(param.to_xml())
        return bean

    def __repr__(self):
        return self.to_xml().toxml()
