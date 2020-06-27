from typing import Optional, Any, Dict, List, Union

from di import Ref, Context


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


def bean(id: Optional[Union[str, type]] = None,
         singleton: bool = True,
         refs: Optional[Dict[str, Ref]] = None,
         consts: Optional[Dict[str, Any]] = None,
         group: str = 'default'):
    """定义bean，并可指定分组。默认分组default。"""
    if type(id) is type:
        _collections.setdefault(group, []).append(RegisterInfo(
            id=None, singleton=singleton, refs=refs, consts=consts, cls=id
        ))
        return id
    else:
        def wrapper(cls):
            _collections.setdefault(group, []).append(RegisterInfo(
                id=id, singleton=singleton, refs=refs, consts=consts,
                cls=cls
            ))
            return cls

        return wrapper


def register_group(ctx: Context, group: str = 'default'):
    for ri in _collections.get(group, []):
        ctx.register(
            cls=ri.cls,
            refs=ri.refs,
            consts=ri.consts,
            singleton=ri.singleton,
            id=ri.id,
        )
