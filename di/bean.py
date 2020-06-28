import enum
# noinspection PyUnresolvedReferences
import json

import xml.dom.minidom
from typing import Union, Any, List

from di.ref import Ref


class PropertyType(str, enum.Enum):
    Const = "const"
    Ref = "ref"


class Property:

    def __init__(self, name: str, type: PropertyType, value: Union[Any, Ref]):
        self.name = name
        self.type = type
        self.value = value

    def to_xml(self):
        elem = xml.dom.minidom.Document().createElement('property')
        elem.setAttribute("name", self.name)

        if self.type is PropertyType.Ref:
            elem.setAttribute("ref", self.value.to_expr())
        elif self.type is PropertyType.Const:
            elem.setAttribute("value", str(self.value))
            elem.setAttribute("value-type", type(self.value).__name__)
        else:
            raise ValueError("unknown property type")

        return elem

    def __repr__(self):
        return self.to_xml().toxml()


class Bean:

    def __init__(self,
                 cls: str,
                 id: str,
                 singleton: bool,
                 params: List[Property]):
        self.cls = cls
        self.params = params
        self.id = id
        self.singleton = singleton

    def to_xml(self):
        bean = xml.dom.minidom.Document().createElement('bean')
        bean.setAttribute("cls", self.cls)
        bean.setAttribute("id", self.id)
        bean.setAttribute("singleton", json.dumps(self.singleton))

        for param in self.params:
            bean.appendChild(param.to_xml())
        return bean

    def __repr__(self):
        return self.to_xml().toxml()
