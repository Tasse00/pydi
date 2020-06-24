import abc
import enum
import inspect
import logging
from functools import partial
from typing import Optional, Dict, List, Any, Union


class RefType(int, enum.Enum):
    Id = 1
    Cls = 2


class Ref(abc.ABC):
    def __init__(self, type: RefType, target: str):
        self.type = type
        self.target = target

    @abc.abstractmethod
    def isDepNode(self, bean) -> bool:
        pass

    def __eq__(self, other):
        return self.type == other.type and self.target == other.target

    def __hash__(self):
        return hash("{}||{}".format(self.type, self.target))

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.target)


class Bean:
    def __init__(self, cls: type, singleton: bool, id: str, params: Dict[str, Union[Ref, Any]]):
        self.cls = cls
        self.params = params
        self.id = id
        self.singleton = singleton

    def __repr__(self):
        return "<Bean id=%s singleton=%s cls=%s self.params=%s>" % (
            self.id, self.singleton, self.cls.__qualname__, self.params)


class IdRef(Ref):
    def __init__(self, tgt: str):
        super(IdRef, self).__init__(RefType.Id, tgt)

    def isDepNode(self, bean: Bean) -> bool:
        return bean.id == self.target


class ClsRef(Ref):
    def __init__(self, tgt: Union[type, str]):
        if isinstance(tgt, type):
            tgt = tgt.__qualname__
        super(ClsRef, self).__init__(RefType.Cls, tgt)

    def isDepNode(self, bean: Bean) -> bool:
        return bean.cls.__qualname__ == self.target


class Context:

    def __init__(self):
        self.id_map: Dict[str, Bean] = {}
        self.cls_map: Dict[str, List[Bean]] = {}
        self.singleton_cache: Dict[Ref, Any] = {}
        self.logger = logging.getLogger(__name__ + "-" + str(id(self))[:4])

    def _get_cls_name(self, cls: type) -> str:
        return cls.__qualname__

    def _auto_detect_cls_param_refs(self, cls: type) -> Dict[str, Ref]:
        """探测目标类初始化参数中的Ref,采用ClsRef策略，并排除基本类型．"""
        return {
            p.name: ClsRef(p.annotation)
            for p in
            inspect.signature(cls).parameters.values()
            if p.default == inspect._empty and p.annotation not in (int, float, str, dict, list, tuple, set)
        }

    def register(self,
                 cls: type,
                 singleton: bool = True,
                 id: Optional[str] = None,
                 refs: Optional[Dict[str, Ref]] = None,
                 consts: Optional[Dict[str, Any]] = None):
        """注册Bean"""
        id = id or self._get_cls_name(cls)

        params = self._auto_detect_cls_param_refs(cls)
        if refs:
            params.update(refs)
        if consts:
            params.update(consts)

        if id in self.id_map:
            raise ValueError("ID {} existed.".format(id))
        bean = Bean(cls=cls, id=id, params=params, singleton=singleton)

        self.id_map[id] = bean
        self.cls_map.setdefault(self._get_cls_name(cls), []).append(bean)

    def _find_bean(self, ref: Ref) -> Bean:
        """通过ref找到对于的bean"""
        valid = list(filter(lambda dn: ref.isDepNode(dn), self.id_map.values()))
        if len(valid) == 0:
            raise ValueError("Ref [{}] not existed.".format(ref))
        elif len(valid) > 1:
            raise ValueError("Ref [{}] has multi DepNodes {}".format(ref, valid))
        else:
            return valid[0]

    def _get_singleton_cache(self, ref: Ref) -> Optional[Any]:
        """获取singleton缓存"""
        return self.singleton_cache.get(ref, None)

    def _set_singleton_cache(self, ref: Ref, ins: Any):
        """设置singleton缓存"""
        self.singleton_cache[ref] = ins

    def _pre_check_instance_params(self, cls: type, params: Dict[str, Any]):
        """检查参数是否满足目标初始化需求"""
        for v in inspect.signature(cls).parameters.values():
            if v.default == inspect._empty:
                if v.name not in params:
                    raise ValueError("Lack of initial param %s for %s" % (v.name, cls))

    def instance(self, ref: Ref, chain_depth: int = 1) -> Any:
        """获取实例对象"""
        tgt = self._find_bean(ref)

        def log(level, msg):
            getattr(self.logger, level)(" " + ">" * chain_depth + ' ' + msg)

        debug = partial(log, level='debug')

        if tgt.singleton and self._get_singleton_cache(ref):
            debug("retrieved {}".format(tgt))
            return self._get_singleton_cache(ref)

        debug("instancing {}".format(tgt))

        params = {pname: (self.instance(pval, chain_depth + 1) if isinstance(pval, Ref) else pval) for pname, pval in
                  tgt.params.items()}
        self._pre_check_instance_params(tgt.cls, params)
        ins = tgt.cls(**params)

        self._set_singleton_cache(ref, ins)

        debug("instanced {}".format(tgt))

        return ins

    def instance_by_id(self, id: str):
        return self.instance(IdRef(id))

    def instance_by_cls(self, cls: type):
        return self.instance(ClsRef(cls))


def NewContext() -> Context:
    return Context()


__all__ = ["NewContext"]
