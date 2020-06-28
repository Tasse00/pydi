from typing import Optional, Any, Dict, List, Union

from di.ref import Ref


class RegisterInfo:
    def __init__(self,
                 cls: type,
                 id: Optional[str] = None,
                 singleton: bool = True,
                 refs: Optional[Dict[str, Ref]] = None,
                 consts: Optional[Dict[str, Any]] = None):
        self.cls = cls
        self.id = id
        self.singleton = singleton
        self.refs = refs
        self.consts = consts


_collections: Dict[str, List[RegisterInfo]] = {}
# _collected_instance: Dict[str, type] = {}

def get_collected_group(group: str) -> List[RegisterInfo]:
    return _collections.get(group, [])


def bean(id: Optional[Union[str, type]] = None,
         singleton: bool = True,
         refs: Optional[Dict[str, Ref]] = None,
         consts: Optional[Dict[str, Any]] = None,
         group: str = 'default'):
    """定义bean，并可指定分组。默认分组default。"""

    def collect(group: str, id: Optional[str], singleton: bool, refs: Optional[Dict[str, Ref]], consts: Optional[Dict[str, Any]], cls: type):
        _collections.setdefault(group, []).append(RegisterInfo(
            id=id, singleton=singleton, refs=refs, consts=consts, cls=cls
        ))

    if type(id) is type:
        collect(group=group, id=None, singleton=singleton, refs=refs,consts=consts,cls=id)
        return id
    else:
        def wrapper(cls):
            collect(group=group, id=id, singleton=singleton, refs=refs, consts=consts, cls=cls)
            return cls
        return wrapper
